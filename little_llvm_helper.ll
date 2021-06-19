@.str = private unnamed_addr constant [13 x i8] c"hello world\0A\00"

@formatInt = private constant [4 x i8] c"%d\0A\00"
@formatFloat = private constant [4 x i8] c"%f\0A\00"
@formatChar = private constant [4 x i8] c"%c\0A\00"

@charInput = private constant [2 x i8] c"%c"
@intInput = private constant [2 x i8] c"%d"

@char.0.0 = global i8 0
@int.0.0 = global i32 0

declare i32 @printf(i8*, ...) nounwind
declare i32 @scanf(i8*, ...) nounwind
; External declaration of the puts function

; Definition of main function
define i32 @main() {   ; i32()*
entry:
  ; Convert [13 x i8]* to i8*...
  ;%x = shl i32 2, 3
;   %q = alloca float ;ptr
;   store float 3.1, float* %q ;save to mem
;   %q = load float, float* %q
  
  %x = fadd double 1.3, 1.3
  %aaa = add i1 0, 0
  ;%ptr = alloca double, double 1.0                               
  %ccc = fadd double 1.0, %x
  ;store double %ccc, double* %ptr
  %cc = alloca i32, i32 97
  
  %c = add i32 97, 1
  
  store i32 %c, i32* %cc
    
  %call.0 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([2 x i8], [2 x i8]* @intInput, i32 0, i32 0), i32* @int.0.0)
  
  %da = load i32, i32* @int.0.0
  
  ; Call puts function to write out the string to stdout.
  ;%call = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @formatInt, i32 0, i32 0), i32 %x) ;int
  ;%call = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @formatFloat, i32 0, i32 0), double %x) ;float
  %call = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @formatInt, i32 0, i32 0), i32 %da) ;char
  ret i32 0
}

