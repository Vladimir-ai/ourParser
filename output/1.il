.assembly extern mscorlib {
.publickeytoken = (B0 3F 5F 7F 11 D5 0A 3A )                         // .?_....:
.ver 5:0:7:0
}
.assembly program
{
}
.class private auto ansi beforefieldinit Program extends [mscorlib]System.Object
{
.method private hidebysig static int32 plus(int32 a, int32 b) cil managed
{
.maxstack  8
.locals init ()
ldarg.s  a
ldarg.s  b
add
ret
}
.method private hidebysig static char[] give_me_ascii() cil managed
{
.maxstack  8
.locals init ([0] char[] ascii, [1] int32 i)
ldc.i4    0x80
newarr    [mscorlib]System.Char
stloc.s   ascii
ldc.i4    0x1
stloc.s   i
br.s  IL_FOR_CTRL_1
IL_FOR_BODY_1: nop
ldloc.s   ascii
ldloc.s  i
ldc.i4    0x1
sub
ldloc.s  i
conv.u2
stelem.i2
ldloc.s  i
ldc.i4    0x1
add
stloc.s   i
IL_FOR_CTRL_1: nop
ldloc.s  i
ldc.i4    0x80
clt
brtrue.s  IL_FOR_BODY_1
ldloc.s  ascii
ret
}
.method private hidebysig static void main() cil managed
{
.entrypoint
.maxstack  8
.locals init ([0] int32 a, [1] int32 b, [2] int32 d, [3] int32 i, [4] int32 j, [5] char ch)
ldc.i4    0x1
stloc.s   a
ldc.i4    0x1
stloc.s   b
ldc.r4    4.1
ldc.i4    0x4
conv.r4
and
conv.i4
stloc.s   d
ldc.i4    0x4
stloc.s   i
br.s  IL_FOR_CTRL_2
IL_FOR_BODY_2: nop
ldc.i4    0x3
stloc.s   j
br.s  IL_FOR_CTRL_3
IL_FOR_BODY_3: nop
ldloc.s  i
ldloc.s  j
call   int32 Program::plus(int32, int32)
call   void [mscorlib]System.Console::WriteLine(int32)
ldloc.s  j
ldc.i4    0x1
sub
stloc.s   j
IL_FOR_CTRL_3: nop
ldloc.s  j
ldc.i4    0x0
cgt
brtrue.s  IL_FOR_BODY_3
ldloc.s  i
ldc.i4    0x1
sub
stloc.s   i
IL_FOR_CTRL_2: nop
ldloc.s  i
ldc.i4    0x0
cgt
brtrue.s  IL_FOR_BODY_2
call   char[] Program::give_me_ascii()
call   void [mscorlib]System.Console::WriteLine(char[])
ldc.i4.s    99
stloc.s   ch
nop
ret
}
}