load harness

@test "extratests-1" {
  check '2 + 3 - 4' '1'
}

@test "extratests-2" {
  check '3 / 2' '1.5'
}

@test "extratests-3" {
  check '5 % 2' '1'
}

@test "extratests-4" {
  check '5 * 6 + 9 % 39' '39'
}

@test "extratests-5" {
  check '5 * 8 + 6 * 4 / -2' '28.0'
}