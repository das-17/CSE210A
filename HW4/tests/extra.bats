load harness

@test "extra-1" {
  check 'x := 1' '⇒ skip, {x → 1}'
}

@test "extra-2" {
  check 'if x = 0 then x := 1 else x := 2' '⇒ x := 1, {}
⇒ skip, {x → 1}'
}

@test "extra-3" {
  check 'while false do x := 100' '⇒ skip, {}'
}

@test "extra-4" {
   check 'x := 10 ; y := 5 ; x := x + y ; y := x - y ; x := x - y' '⇒ skip; y := 5; x := (x+y); y := (x-y); x := (x-y), {x → 10}
⇒ y := 5; x := (x+y); y := (x-y); x := (x-y), {x → 10}
⇒ skip; x := (x+y); y := (x-y); x := (x-y), {x → 10, y → 5}
⇒ x := (x+y); y := (x-y); x := (x-y), {x → 10, y → 5}
⇒ skip; y := (x-y); x := (x-y), {x → 15, y → 5}
⇒ y := (x-y); x := (x-y), {x → 15, y → 5}
⇒ skip; x := (x-y), {x → 15, y → 10}
⇒ x := (x-y), {x → 15, y → 10}
⇒ skip, {x → 5, y → 10}'
}

@test "extra-5" {
    check 'if x=0 then x:= 4 else x:= 3' '⇒ x := 4, {}
⇒ skip, {x → 4}'
}