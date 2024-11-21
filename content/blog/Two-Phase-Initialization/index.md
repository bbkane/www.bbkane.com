+++
title = "Two Phase Initialization"
date = 2024-11-20
+++

I recently ran into two phase initialization at work but didn't remember the name. Basically, two phase initialization looks like this:

```go
type Object struct {
	Res Resource
}

func NewObject() *Object {
	return &Object{}
}

func (o *Object) Init() {
  o.Res = InitializeResource()
}
```

Why is this bad? Because anyone who wants an `Object` needs to remember to call two functions, instead of just the one. This can be especially bad in a concurrent environment if another goroutine trys to access the objected created by `NewObject` before `Init` is run.

Options to fix this include:

- create `Res` inside of `NewObject`
- make `res Res` a parameter of `NewObject`

In either case, the object is completely constructed by the end of `NewObject` and you can just use it. I haven't found a good reason to use two phase initialization in Go.

Other resources:

- [One-Stage and Two-Stage Construction of Objects | Microsoft Learn](https://learn.microsoft.com/en-us/cpp/mfc/one-stage-and-two-stage-construction-of-objects?view=msvc-170) - this explains why this Microsoft author actually prefers two phase initialization in C++. This is countered by the [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rnr-two-phase-init), which argue you should still avoid it.
- [Is Two-Step Initialization a Solution or a Symptom?](https://www.yegor256.com/2023/08/08/two-step-initialization.html) - explains Java-specific problems with two phase initialization

