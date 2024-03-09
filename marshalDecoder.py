import re
import argparse
import codecs
import subprocess

class PycDecompiler:
    PYTHON_MAGIC = {
           # Python 1

    20121: (1, 5),

    50428: (1, 6),



    # Python 2

    50823: (2, 0),

    60202: (2, 1),

    60717: (2, 2),

    62011: (2, 3),  # a0

    62021: (2, 3),  # a0

    62041: (2, 4),  # a0

    62051: (2, 4),  # a3

    62061: (2, 4),  # b1

    62071: (2, 5),  # a0

    62081: (2, 5),  # a0

    62091: (2, 5),  # a0

    62092: (2, 5),  # a0

    62101: (2, 5),  # b3

    62111: (2, 5),  # b3

    62121: (2, 5),  # c1

    62131: (2, 5),  # c2

    62151: (2, 6),  # a0

    62161: (2, 6),  # a1

    62171: (2, 7),  # a0

    62181: (2, 7),  # a0

    62191: (2, 7),  # a0

    62201: (2, 7),  # a0

    62211: (2, 7),  # a0



    # Python 3

    3000: (3, 0),

    3010: (3, 0),

    3020: (3, 0),

    3030: (3, 0),

    3040: (3, 0),

    3050: (3, 0),

    3060: (3, 0),

    3061: (3, 0),

    3071: (3, 0),

    3081: (3, 0),

    3091: (3, 0),

    3101: (3, 0),

    3103: (3, 0),

    3111: (3, 0),  # a4

    3131: (3, 0),  # a5



    # Python 3.1

    3141: (3, 1),  # a0

    3151: (3, 1),  # a0



    # Python 3.2

    3160: (3, 2),  # a0

    3170: (3, 2),  # a1

    3180: (3, 2),  # a2



    # Python 3.3

    3190: (3, 3),  # a0

    3200: (3, 3),  # a0

    3220: (3, 3),  # a1

    3230: (3, 3),  # a4



    # Python 3.4

    3250: (3, 4),  # a1

    3260: (3, 4),  # a1

    3270: (3, 4),  # a1

    3280: (3, 4),  # a1

    3290: (3, 4),  # a4

    3300: (3, 4),  # a4

    3310: (3, 4),  # rc2



    # Python 3.5

    3320: (3, 5),  # a0

    3330: (3, 5),  # b1

    3340: (3, 5),  # b2

    3350: (3, 5),  # b2

    3351: (3, 5),  # 3.5.2



    # Python 3.6

    3360: (3, 6),  # a0

    3361: (3, 6),  # a0

    3370: (3, 6),  # a1

    3371: (3, 6),  # a1

    3372: (3, 6),  # a1

    3373: (3, 6),  # b1

    3375: (3, 6),  # b1

    3376: (3, 6),  # b1

    3377: (3, 6),  # b1

    3378: (3, 6),  # b2

    3379: (3, 6),  # rc1



    # Python 3.7

    3390: (3, 7),  # a1

    3391: (3, 7),  # a2

    3392: (3, 7),  # a4

    3393: (3, 7),  # b1

    3394: (3, 7),  # b5



    # Python 3.8

    3400: (3, 8),  # a1

    3401: (3, 8),  # a1

    3410: (3, 8),  # a1

    3411: (3, 8),  # b2

    3412: (3, 8),  # b2

    3413: (3, 8),  # b4



    # Python 3.9

    3420: (3, 9),  # a0

    3421: (3, 9),  # a0

    3422: (3, 9),  # a0

    3423: (3, 9),  # a2

    3424: (3, 9),  # a2

    3425: (3, 9),  # a2
    }

    def __init__(self, file_path, output_path=None):
        self.file_path = file_path
        self.output_path = output_path

    def get_magic_code(self, code):
        pattern = r'loads\([b][\'\"](.*?)[\'\"]\)\)'
        matches = re.findall(pattern, code, re.DOTALL)
        return codecs.escape_decode(matches[0].strip())[0]

    def run_bash(self, bash_command):
        try:
            result = subprocess.check_output(bash_command, shell=True, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            result = e.output
        return result

    def create_pyc_file(self, magic, mar_com, marshal_code):
        with open("pycfile.pyc", "wb") as f:
            f.write(magic + mar_com + marshal_code)

    def decompile_and_save(self, version, _):
        outputs = self.run_bash(f"./pycdc pycfile.pyc -v {version}.{_}")
        if outputs.count('\n') >= 3:
            print(outputs)
            with open(self.output_path, "w") as f:
                f.write(outputs)
        self.run_bash("rm pycfile.pyc")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a file with multiple options.')
    parser.add_argument('-f', '--file', metavar='FILE', help='Specify the path to the input file', required=True)
    parser.add_argument('-o', '--output', metavar='OUTPUT_FILE', help='Specify the path to the output file')
    args = parser.parse_args()

    decompiler = PycDecompiler(args.file, args.output)
    code = open(args.file, "r").read()
    marshal_code = decompiler.get_magic_code(code)

    mar3_com = b"\x0D\x0A\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff"
    mar2_com = b"\x0D\x0A\xD5\x65\xDA\x65"

    for key, (version, _) in decompiler.PYTHON_MAGIC.items():
        magic = key.to_bytes(2, byteorder="little")
        decompiler.create_pyc_file(magic, mar2_com if version == 2 else mar3_com, marshal_code)
        decompiler.decompile_and_save(version, _)
