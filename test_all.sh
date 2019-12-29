#! /bin/bash
sage -c 'load("check_license.py")'
case $? in
    42)
    # No license
        exit 0
        ;;
    0)
        # Has license
        sage -c 'load("patch_into_sage_module.py")' || exit 1
        sage -c 'load("sage check_get_solver_with_name.py")' || exit 1
        sage -c 'load("check_sage_testsuite.py")' || echo "Ignoring errors from the sage test suite"
        exit 0
        ;;
    *)
        # Other error
        exit 1
esac
