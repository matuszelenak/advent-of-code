println(java.io.File("1a.in").readLines().map { it.toInt() }.zipWithNext { curr, next -> next > curr }.count { it })
