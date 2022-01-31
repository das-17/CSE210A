load harness

@test "extra-1" {
  check 'a := true? 1 : 2' '{a → 1}'
}

@test "extra-2" {
  check 'a18b := false ? 0 : 1234' '{a18b → 1234}'
}

@test "extra-3" {
  check 'a := 5 < 20 ? 5 + 4 : 5 - 4' '{a → 9}'
  
}

@test "extra-4" {
    check 'a := -1 * -2 = 2 ?  1 : 0' '{a → 1}'
  
}

@test "extra-5" {
  check 'a := 5 % 4 = 0 ? 10 : 100' '{a → 100}'
}