java.io.File("3a.in").readLines().map { line ->
    line.map { mapOf('0' to -1, '1' to 1)[it]!! }
}.reduce { acc, elem -> acc.zip(elem).map { it.first + it.second } }.let { arr ->
    arr.joinToString("") { if (it > 0) "1" else "0" }.toInt(2) * arr.joinToString("") { if (it > 0) "0" else "1" }.toInt(2)
}