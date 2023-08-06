# img2array

Prints the pixels of an image into an array of RGB values.
This can be copied easily to other applications, such as embedded apps.

# Commands

-h, --help    :  Help text  
-i, --image   :  Image file path  
-p, --prefix  :  Prefix for the item, like "colorFunc\("  
-P, --postfix :  Postfix for the item, like "\)"  
-f, --format  :  Format of the color, defaults to RGB. Possible values: RGB, RGBA, Hex, HexAlpha  

# Install

`pip install img2array`

# Example

`img2array -i file.png --prefix=coolFunction\( --postfix=\) --format=RGB`

**Note**: the \ before () may be required or not depending on the shell you're using.

This should print an array version of the image like

```
{
    {coolFunction(200,200,200), coolFunction(123,123,123)},
    {coolFunction(111,111,111), coolFunction(41,0,12)}
}
```

You can then easily copy-paste this to your applications.