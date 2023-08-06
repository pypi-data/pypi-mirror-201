import sys
import getopt
from img2array.img2array import img2array

def main():
    help_text = """
    Prints the pixels of an image into an array of RGB values.
    This can be copied easily to other applications, such as embedded apps.

    Commands:
        -h, --help    :  This help text
        -i, --image   :  Image file path
        -p, --prefix  :  Prefix for the item, like "colorFunc\\("
        -P, --postfix :  Postfix for the item, like "\\)"
        -f, --format  :  Format of the color, defaults to RGB. Possible values: RGB, RGBA, Hex, HexAlpha

    Example:
        img2array -i file.png --prefix=coolFunction\\( --postfix=\\) --format=RGB

        Note: the \\ before () may be required or not depending on the shell you're using.

        This should print an array version of the image like
        {
            {coolFunction(200,200,200), coolFunction(123,123,123)},
            {coolFunction(111,111,111), coolFunction(41,0,12)}
        }

        You can then easily copy-paste this to your applications.
    """

    argv = sys.argv[1:]
    if len(argv) <= 0:
        print("No input data given, printing help!")
        print(help_text)
        sys.exit(-1)

    image_path = ""
    item_prefix = ""
    item_postfix = ""
    color_format = "RGB"

    opts, args = getopt.getopt(
        argv, "hi:p:P:f:", ["help", "image=", "prefix=", "postfix=", "format="]
    )

    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print(help_text)
            sys.exit(0)
        elif opt in ("-i", "--image"):
            image_path = arg
        elif opt in ("-p", "--prefix"):
            item_prefix = arg
        elif opt in ("-P", "--postfix"):
            item_postfix = arg
        elif opt in ("-f", "--format"):
            color_format = arg

    i2a = img2array(image_path, item_prefix, item_postfix, color_format)
    i2a.run()
