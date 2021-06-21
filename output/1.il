.assembly extern mscorelib {
.publickeytoken = (B0 3F 5F 7F 11 D5 0A 3A )                         // .?_....:
.ver 5:0:7:0
}
.assembly program
{
}
.class private auto ansi beforefieldinit Program extends [mscorelib]System.Object
{
.method private hidebysig static void main() cil managed
{
.entrypoint
.maxstack  8
.locals init ([0] bool a, [1] bool b, [2] int32 d, [3] char ch)
ldc.r4    0.1
ldc.r4    0.0
ceq
ldc.i4.0
ceq
stloc.s   a
ldc.i4    0x1
ldc.i4.0
ceq
ldc.i4.0
ceq
stloc.s   b
ldc.r4    4.1
ldc.i4    0x4
conv.r4
and
conv.i4
stloc.s   d
ldc.i4.s    99
stloc.s   ch
nop
ret
}
}