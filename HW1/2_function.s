	.arch armv7-a
	.fpu vfp
	.eabi_attribute 28, 1
	.eabi_attribute 20, 1
	.eabi_attribute 21, 1
	.eabi_attribute 23, 3
	.eabi_attribute 24, 1
	.eabi_attribute 25, 1
	.eabi_attribute 26, 2
	.eabi_attribute 30, 6
	.eabi_attribute 34, 1
	.eabi_attribute 18, 4
	.file	"2_function.cc"
	.text
	.align	2
	.global	_Z9sum_arrayPi
	.syntax unified
	.arm
	.type	_Z9sum_arrayPi, %function
_Z9sum_arrayPi:
	.fnstart
.LFB0:
	@ args = 0, pretend = 0, frame = 16
	@ frame_needed = 1, uses_anonymous_args = 0
	@ link register save eliminated.
	str	fp, [sp, #-4]!
	add	fp, sp, #0
	sub	sp, sp, #20
	str	r0, [fp, #-16]
	mov	r3, #0
	str	r3, [fp, #-8]
	ldr	r3, [fp, #-16]
	ldr	r3, [r3]
	cmp	r3, #99
	bgt	.L2
	ldr	r3, [fp, #-16]
	ldr	r2, [r3]
	ldr	r3, [fp, #-16]
	add	r3, r3, #4
	ldr	r3, [r3]
	add	r2, r2, r3
	ldr	r3, [fp, #-16]
	add	r3, r3, #8
	ldr	r3, [r3]
	add	r3, r2, r3
	str	r3, [fp, #-8]
.L2:
	ldr	r3, [fp, #-8]
	mov	r0, r3
	add	sp, fp, #0
	@ sp needed
	ldr	fp, [sp], #4
	bx	lr
	.cantunwind
	.fnend
	.size	_Z9sum_arrayPi, .-_Z9sum_arrayPi
	.ident	"GCC: (SUSE Linux) 14.3.0"
	.section	.note.GNU-stack,"",%progbits
