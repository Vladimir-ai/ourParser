.assembly extern mscorlib {
.publickeytoken = (B0 3F 5F 7F 11 D5 0A 3A )                         // .?_....:
.ver 5:0:7:0
}
.assembly program
{
}
.class private auto ansi beforefieldinit Program extends [mscorlib]System.Object
{
.method private hidebysig static int32 main() cil managed
{
.entrypoint
.maxstack  8
.locals init ([0] int32[] df, [1] int32 fg)
ldc.i4    0x3
newarr    [mscorlib]System.Int32
stloc.s   df
ldloc.s  df
ldc.i4    0x1
ldelem.i4
stloc.s   fg
ldc.i4    0x0
ret
}
}