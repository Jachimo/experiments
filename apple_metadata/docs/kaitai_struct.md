Notes on kaitai_struct
======================

[kaitai_struct on Github](https://github.com/kaitai-io/kaitai_struct)

> Kaitai Struct (KS) is a declarative language used to describe various binary data structures, laid out in files or in memory: i.e. binary file formats, network stream packet formats, etc.

> The main idea is that a particular format is described in Kaitai Struct language (.ksy file) only once and then can be compiled with kaitai-struct-compiler (or ksc for short) into source files in one of the supported programming languages. These modules will include generated code for a parser that can read the described data structure from a file or stream and provide access to it in a nice, easy-to-comprehend API.

AppleSingle/AppleDouble is one of the formats in their online [format gallery][1], with both the Kaitai DSL input definition, and the output libraries in a bunch of languages, available.

The file `apple_single_double.py` is pulled directly from [the format's Python download page][2] with minimal changes.

[1]: https://formats.kaitai.io/
[2]: https://formats.kaitai.io/apple_single_double/python.html
