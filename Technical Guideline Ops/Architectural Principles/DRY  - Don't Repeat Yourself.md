# DRY - Don't Repeat Yourself

> [!info] Purpose
> DRY (Don't Repeat Yourself) is a fundamental software engineering principle: every piece of knowledge should have a single, authoritative representation in your system. This guide provides tool-agnostic patterns for eliminating duplication across SQL, Python, and data platform development.

## Overview

**Don't Repeat Yourself** means extracting reusable logic, calculations, and patterns into centralized, maintainable components. When you find yourself copying code, ask: "Can this be abstracted into a function, module, or shared artifact?"

## Why DRY Matters

**Single source of truth:** Changes propagate automatically everywhere - no risk of inconsistent implementations or desynchronized business rules.
**Reduced maintenance:** Update once instead of hunting through N files. Fewer places for bugs to hide, easier code reviews.
**Improved testing:** Test the shared component once; all consumers inherit the fix automatically.
**Better collaboration:** Team members reuse proven patterns. Knowledge stays centralized and documented for faster onboarding.

## When to Break DRY

**Don't over-abstract** - sometimes duplication is acceptable.
### Acceptable Duplication Scenarios

| Scenario                 | Reason to Duplicate                                               |
| ------------------------ | ----------------------------------------------------------------- |
| **One-time use**         | If logic appears only once, inline it for clarity                 |
| **Different contexts**   | Similar code with different business meaning shouldn't be unified |
| **Performance-critical** | Abstraction overhead may hurt performance                         |
| **Temporary code**       | Exploratory analysis or POC code can duplicate temporarily        |
| **Clear readability**    | Sometimes explicit duplication is more readable than abstraction  |

## DRY Checklist

Before writing code, ask yourself:

- [ ] Have I seen this pattern before in the project?
- [ ] Will other parts of the codebase need this logic?
- [ ] Does a shared utility/function already exist?
- [ ] Would abstraction make this more maintainable?
- [ ] Is this the third occurrence (Rule of Three)?
- [ ] Will the abstraction be easy to understand?
- [ ] Does performance allow for abstraction?
