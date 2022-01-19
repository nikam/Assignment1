load harness

@test "test-1" {
  check '3 * 7 + 3' '24'
}

@test "test-2" {
  check '5 + 2 * 2' '9'
}


@test "test-3" {
  check '3 + -3' '0'
}

@test "test-4" {
  check '1   +       6' '7'
}

@test "test-5" {
  check '-2 - -4' '2'
}

@test "test-6" {
  check '15 + 1 * 6 - 9 / 3' '18.0'
}


