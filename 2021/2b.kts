java.io.File("2a.in").readLines().fold(Triple(0, 0, 0)) { (x, y, a), line ->
    val (cmd, delta) = line.split(' ')
    when (cmd) {
        "forward" -> Triple(x + delta.toInt(), y + a * delta.toInt(), a)
        "down" -> Triple(x, y, a + delta.toInt())
        "up" -> Triple(x, y, a - delta.toInt())
        else -> Triple(x, y, a)
    }
}.let { it.first * it.second }