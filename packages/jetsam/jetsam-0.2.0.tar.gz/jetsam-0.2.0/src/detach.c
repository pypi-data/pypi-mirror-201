/* Heavily inspired by nix-processmgmt (MIT License)
 * https://github.com/svanderburg/nix-processmgmt/blob/master/webapp/daemonize.c
 */
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <fcntl.h>
#include <signal.h>
#include <stdbool.h>
#include <stdint.h>
#include <sys/resource.h>
// #include <sys/time.h>
#include "log.h"

// Both Linux and MacOS have /dev/null
#define DEV_NULL_PATH ("/dev/null")

/// NOTE: functions have external linkage by default. "static" == internal linkage 

// Similar to file descriptors, the daemon process also inherits the signal
// handler configuration of the caller process. If signal handlers have been
// altered, then the daemon process may behave in a non-standard and unpredictable
// way.
// 
// For example, the TERM signal handler could have been overridden so that the
// daemon no longer cleanly shuts down when it receives a TERM signal. As a
// countermeasure, the signal handlers must be reset to their default behavior.
//
static void reset_signal_handlers_to_default() {
    for (int i = 1; i < NSIG; i++) {
        // SIGKILL and SIGSTOP cannot be overridden
        if (i != SIGKILL && i != SIGSTOP) {
            signal(i, SIG_DFL);
        }
    }
}

// Resetting the signal mask
// It is also possible to completely block certain signals by adjusting
// the signal mask. The signal mask also gets inherited by the daemon
// from the calling process. To make a daemon act predictably, e.g. it
// should do a proper shutdown when it receives the TERM signal, it would
// be a good thing to reset the signal mask to the default configuration.
//
static bool clear_signal_mask() {
    sigset_t set;
    return ((sigemptyset(&set) == 0) && (sigprocmask(SIG_SETMASK, &set, NULL) == 0));
}

// Closing all file descriptors, except the standard ones: stdin, stdout, stderr
//
// Closing all, but the standard file descriptors, is a good practice, because the
// daemon process inherits all open files from the calling process
// (e.g. the shell session from which the daemon is invoked).
//
// Not closing any additional open file descriptors may cause the file descriptors
// to remain open for an indefinite amount of time, making it impossible to cleanly
// unmount the partition where these files may have been stored. Moreover, it also
// keeps file descriptors unnecessarily allocated.
//
// The daemon manual page describes two strategies to implement closing these
// non-standard file descriptors. On Linux, it is possible to iterate over the content
// of the: /proc/self/fd file. A portable, but less efficient, way is to iterate from
// file descriptor 3 to the value returned by getrlimit for RLIMIT_NOFILE.
//
static bool close_non_standard_file_descriptors() {
    struct rlimit rlim;
    int num_of_fds = getrlimit(RLIMIT_NOFILE, &rlim);

    if (num_of_fds == -1)
        return false;

    for (int i = 3; i < num_of_fds; i++) {
        close(i);
    }

    return true;
}

// Connecting /dev/null to standard input, output and error in the daemon process
// Since we have detached from the terminal, we should connect /dev/null to the
// standard file descriptors in the daemon process, because these file descriptors
// are still connected to the terminal from which we have detached.
//
static int attach_standard_file_descriptors_to_null() {
    int null_fd_read;
    int null_fd_write;
    int retval = 0;

    retval |= (null_fd_read = open(DEV_NULL_PATH, O_RDONLY)) != -1;
    retval |= (null_fd_write = open(DEV_NULL_PATH, O_WRONLY)) != -1;
    retval |= dup2(null_fd_read, STDIN_FILENO) != -1;
    retval |= dup2(null_fd_write, STDOUT_FILENO) != -1;
    retval |= dup2(null_fd_write, STDERR_FILENO) != -1;

    return retval;
}

// Clean up environment and spawn new interpreter
static void run_detached(char const *func_name, PyObject *callback, char const *logfile) {
    log_init(logfile); // all daemons append to the same file

    if (!clear_signal_mask()) {
        log_error("ERROR: Unable to clear signal mask");
        return;
    }

    reset_signal_handlers_to_default();

    if (!close_non_standard_file_descriptors()) {
        log_error("ERROR: unable to close non standard fds");
        return;
    }


    if (!attach_standard_file_descriptors_to_null()) {
        log_error("ERROR: Cannot attach standard fds to null");
        return;
    }

    // The umask (a setting that globally alters file permissions of newly created files)
    // may have been adjusted by the calling process, causing directories and files
    // created by the daemon to have unpredictable file permissions. As a countermeasure,
    // we should reset the umask to 0 with the following function call:
    umask(0);
 
    if (!log_pid(func_name)) {
        log_error("ERROR: unable to create pid file: %m\n"); // errno
        return;
    }

    // Changing current working directory to / in the daemon process
    // The daemon process also inherits the current working directory
    // of the caller process. It may happen that the current working
    // directory refers to an external drive or partition. As a result,
    // it can no longer be cleanly unmounted while the daemon is running.
    // 
    // To prevent this from happening, we should change the current
    // working directory to the root folder, because that is the only
    // partition that is guaranteed to stay mounted while the system
    // is running:

    // TODO: no matter which parent process 'chdir("/")' happens in 
    // TODO: PyObject_CallObject fails 
    //// if (chdir("/") == -1) {
    ////     error(lg, "ERROR: unable to change directory to '/', %m");
    ////     return;
    //// }

    Py_InitializeEx(0);  // don't register signal handlers


    // TODO: Setup signal handling
    // PyOS_sighandler_t
    // PyOS_setsig()
    // PyObject *global_dict = PyModule_GetDict(PyImport_AddModule("__main__"));
    // PyObject *py_func = PyDict_GetItemString(global_dict, callback);

    PyObject *result = PyObject_CallObject(callback, NULL);
    if (!result) {
        log_error("unable to call function object");
    }

    Py_FinalizeEx();
}


PyObject *detach(PyObject *unused, PyObject *args) {
    PyObject *callback;
    char const *func_name;
    char const *logfile;

    if (!PyArg_ParseTuple(args, "Oss", &callback, &func_name, &logfile)) {
        PyErr_SetString(PyExc_TypeError, "jetsam error: incorrect arguments");
        return NULL;
    }

    if (!PyCallable_Check(callback)) {
        PyErr_SetString(PyExc_TypeError, "jetsam error: a function is required");
        return NULL;
    }

    // PyObject *func_name = PyObject_GetAttrString(callback, "__name__");
    // PyObject_Print(func_name, stdout, Py_PRINT_RAW);

    pid_t pid = fork(); // from this point on (parent and child) are running
    if (pid < 0) {
        PyErr_SetString(PyExc_OSError, "jetsam error: initial fork failed");
        return NULL;
    }

    if (pid > 0) {
        Py_RETURN_NONE; // terminate parent aka return control to python interpreter
    }

    if (pid == 0) { // 1st child process
        // >> Decoupling << https://stackoverflow.com/a/5386753
        // - Session ID is still the same as parent
        // - Setting sid to "this" child process (which will terminate soon) 
        // - Unable to gain a "controlling" terminal (CTTY)
        //
        // ... Thus _true daemon_
        setsid();

        pid = fork(); // double fork magic

        // TODO: catch second failure (not likely)

        if (pid > 0) {
            exit(0); // terminate 2nd parent (C Parent)
        }

        if (pid == 0) { // 2nd child process
            run_detached(func_name, callback, logfile);
        }
    }
    Py_RETURN_NONE;
}

static PyMethodDef detach_method[] = {
    {"detach", detach, METH_VARARGS, "Spawns a truly daemonized python function"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef detach_module = {
    PyModuleDef_HEAD_INIT,
    "detacher",
    "Detach from current process and spawn in the background",
    -1,
    detach_method
};

PyMODINIT_FUNC PyInit_detacher(void) {
    return PyModule_Create(&detach_module);
}
