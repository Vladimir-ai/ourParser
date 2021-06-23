.assembly extern mscorlib {
.publickeytoken = (B0 3F 5F 7F 11 D5 0A 3A )                         // .?_....:
.ver 5:0:7:0
}
.assembly program
{
}
.class private auto ansi beforefieldinit Program extends [mscorlib]System.Object
{
.method private hidebysig static void bubbleSort(int32[] arr, int32 n) cil managed
{
.maxstack  8
.locals init ([0] int32 i, [1] int32 j, [2] int32 tmp)
IL_0xe: ldc.i4    0x0
IL_0xf: stloc.s   i
IL_0x10: br.s  IL_FOR_CTRL_1
IL_FOR_BODY_1: nop
IL_0x12: ldc.i4    0x0
IL_0x13: stloc.s   j
IL_0x14: br.s  IL_FOR_CTRL_2
IL_FOR_BODY_2: nop
IL_0x16: ldarg.s  arr
IL_0x17: ldloc.s  j
IL_0x18: ldelem.i4
IL_0x19: ldarg.s  arr
IL_0x1a: ldloc.s  j
IL_0x1b: ldc.i4    0x1
IL_0x1c: add
IL_0x1d: ldelem.i4
IL_0x1e: cgt
IL_0x1f: brfalse.s IL_IFF3
IL_0x20: ldarg.s  arr
IL_0x21: ldloc.s  j
IL_0x22: ldelem.i4
IL_0x23: stloc.s   tmp
IL_0x24: ldarg.s   arr
IL_0x25: ldloc.s  j
IL_0x26: ldarg.s  arr
IL_0x27: ldloc.s  j
IL_0x28: ldc.i4    0x1
IL_0x29: add
IL_0x2a: ldelem.i4
IL_0x2b: stelem.i4
IL_0x2c: ldarg.s   arr
IL_0x2d: ldloc.s  j
IL_0x2e: ldc.i4    0x1
IL_0x2f: add
IL_0x30: ldloc.s  tmp
IL_0x31: stelem.i4
IL_0x32: br.s IL_IFE3
IL_IFF3: nop
IL_IFE3: nop
IL_0x35: ldloc.s  j
IL_0x36: ldc.i4    0x1
IL_0x37: add
IL_0x38: stloc.s   j
IL_FOR_CTRL_2: nop
IL_0x3a: ldloc.s  j
IL_0x3b: ldarg.s  n
IL_0x3c: ldloc.s  i
IL_0x3d: sub
IL_0x3e: ldc.i4    0x1
IL_0x3f: sub
IL_0x40: clt
IL_0x41: brtrue.s  IL_FOR_BODY_2
IL_0x42: ldloc.s  i
IL_0x43: ldc.i4    0x1
IL_0x44: add
IL_0x45: stloc.s   i
IL_FOR_CTRL_1: nop
IL_0x47: ldloc.s  i
IL_0x48: ldarg.s  n
IL_0x49: ldc.i4    0x1
IL_0x4a: sub
IL_0x4b: clt
IL_0x4c: brtrue.s  IL_FOR_BODY_1
IL_0x4d: nop
IL_0x4e: ret
}
.method private hidebysig static char[] give_me_ascii() cil managed
{
.maxstack  8
.locals init ([0] char[] ascii, [1] int32 i)
IL_0x54: ldc.i4    0x80
IL_0x55: newarr    [mscorlib]System.Char
IL_0x56: stloc.s   ascii
IL_0x57: ldc.i4    0x1
IL_0x58: stloc.s   i
IL_0x59: br.s  IL_FOR_CTRL_4
IL_FOR_BODY_4: nop
IL_0x5b: ldloc.s   ascii
IL_0x5c: ldloc.s  i
IL_0x5d: ldc.i4    0x1
IL_0x5e: sub
IL_0x5f: ldloc.s  i
IL_0x60: conv.u2
IL_0x61: stelem.i2
IL_0x62: ldloc.s  i
IL_0x63: ldc.i4    0x1
IL_0x64: add
IL_0x65: stloc.s   i
IL_FOR_CTRL_4: nop
IL_0x67: ldloc.s  i
IL_0x68: ldc.i4    0x80
IL_0x69: clt
IL_0x6a: brtrue.s  IL_FOR_BODY_4
IL_0x6b: ldloc.s  ascii
IL_0x6c: ret
}
.method private hidebysig static void main() cil managed
{
.entrypoint
.maxstack  8
.locals init ([0] int32 n, [1] int32[] a, [2] int32 i, [3] int32 i, [4] int32 i, [5] char ch)
IL_0x73: ldc.i4    0xa
IL_0x74: stloc.s   n
IL_0x75: ldc.i4    0xa
IL_0x76: newarr    [mscorlib]System.Int32
IL_0x77: stloc.s   a
IL_0x78: ldloc.s  n
IL_0x79: stloc.s   i
IL_0x7a: br.s  IL_FOR_CTRL_5
IL_FOR_BODY_5: nop
IL_0x7c: ldloc.s   a
IL_0x7d: ldloc.s  n
IL_0x7e: ldloc.s  i
IL_0x7f: sub
IL_0x80: ldloc.s  i
IL_0x81: stelem.i4
IL_0x82: ldloc.s  i
IL_0x83: ldc.i4    0x1
IL_0x84: sub
IL_0x85: stloc.s   i
IL_FOR_CTRL_5: nop
IL_0x87: ldloc.s  i
IL_0x88: ldc.i4    0x0
IL_0x89: cgt
IL_0x8a: brtrue.s  IL_FOR_BODY_5
IL_0x8b: ldc.i4    0x0
IL_0x8c: stloc.s   i
IL_0x8d: br.s  IL_FOR_CTRL_6
IL_FOR_BODY_6: nop
IL_0x8f: ldloc.s  a
IL_0x90: ldloc.s  i
IL_0x91: ldelem.i4
IL_0x92: call   void [mscorlib]System.Console::WriteLine(int32)
IL_0x93: ldloc.s  i
IL_0x94: ldc.i4    0x1
IL_0x95: add
IL_0x96: stloc.s   i
IL_FOR_CTRL_6: nop
IL_0x98: ldloc.s  i
IL_0x99: ldloc.s  n
IL_0x9a: clt
IL_0x9b: brtrue.s  IL_FOR_BODY_6
IL_0x9c: ldloc.s  a
IL_0x9d: ldloc.s  n
IL_0x9e: call   void Program::bubbleSort(int32[], int32)
IL_0x9f: ldc.i4    0x0
IL_0xa0: stloc.s   i
IL_0xa1: br.s  IL_FOR_CTRL_7
IL_FOR_BODY_7: nop
IL_0xa3: ldloc.s  a
IL_0xa4: ldloc.s  i
IL_0xa5: ldelem.i4
IL_0xa6: call   void [mscorlib]System.Console::WriteLine(int32)
IL_0xa7: ldloc.s  i
IL_0xa8: ldc.i4    0x1
IL_0xa9: add
IL_0xaa: stloc.s   i
IL_FOR_CTRL_7: nop
IL_0xac: ldloc.s  i
IL_0xad: ldloc.s  n
IL_0xae: clt
IL_0xaf: brtrue.s  IL_FOR_BODY_7
IL_0xb0: ldc.i4.s    99
IL_0xb1: stloc.s   ch
IL_0xb2: nop
IL_0xb3: ret
}
}