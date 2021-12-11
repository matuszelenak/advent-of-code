import java.io.File

val pairs = mapOf(
    ')' to '(',
    ']' to '[',
    '}' to '{',
    '>' to '<'
)
val scores = mapOf(
    ')' to 3, ']' to 57, '}' to 1197, '>' to 25137
)

File("10.in").readLines().map { line ->
    val stack = mutableListOf<Char>()
    for (c in line) {
        if (pairs.containsKey(c)) {
            try {
                stack.removeLast().let {
                    if (it != pairs[c]) throw NoSuchElementException()
                }
            } catch (e: NoSuchElementException) {
                return@map scores[c]!!
            }
        } else stack.add(c)
    }
    0
}.sum()