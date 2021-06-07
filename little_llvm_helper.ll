@.str = private unnamed_addr constant [13 x i8] c"hello world\0A\00"

@formatInt = private constant [3 x i8] c"%d\0A"
@formatFloat = private constant [3 x i8] c"%f\0A"
@formatChar = private constant [3 x i8] c"%c\0A"


declare i32 @printf(i8*, ...) nounwind
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
  %cc = alloca i8, i8 97
  
  %c = add i8 97, 1
  
  store i8 %c, i8* %cc 
  %da = load i8, i8* %cc
  
  
  ; Call puts function to write out the string to stdout.
  ;%call = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @formatInt, i32 0, i32 0), i32 %x) ;int
  ;%call = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @formatFloat, i32 0, i32 0), double %x) ;float
  %call = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @formatChar, i32 0, i32 0), i8 %da) ;char
  ret i32 0
}

