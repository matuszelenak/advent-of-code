java.io.File("2a.in").readLines().fold(0 to 0) { (x, y), line ->
    val (cmd, delta) = line.split(' ')
    when (cmd) {
        "forward" -> x + delta.toInt() to y
        "down" -> x to y + delta.toInt()
        "up" -> x to y - delta.toInt()
        else -> x to y
    }
}.let { it.first * it.second }