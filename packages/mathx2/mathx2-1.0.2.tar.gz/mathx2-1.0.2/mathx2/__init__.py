import itertools
import math

class Mathx2():

    # Dodawanie dwóch liczb
    @staticmethod
    def add(a, b):
        return float(a) + float(b)


    # Sprawdzanie czy dwa wyrazy są anagramami
    @staticmethod
    def isAnagram(a, b):
        a = list(a)
        b = list(b)
        a.sort()
        b.sort()
        return ''.join(a) == ''.join(b)
    

    # Sprawdzanie czy dwa wyrazy są palindromami
    @staticmethod
    def isPalindrome(a, b):
        return a == b[::-1]


    # Liczenie n wyrazu ciągu fibonacciego rekurencyjnie
    @staticmethod
    def fibRecursive(n):
        if n > 2:
            return Mathx2.fibRecursive(n - 1) + Mathx2.fibRecursive(n - 2)
        else:
            return 1


    # Liczenie n wyrazu ciągu fibonacciego iteracyjnie
    @staticmethod
    def fib(n):
        a, b = 0, 1
        for i in range(n):
            a, b = b, a + b
        return a


    # Rozkład liczby PARZYSTEJ na składniki pierwsze - WYMAGA biblioteki itertools
    # np. 22 = 3 + 19 czyli 22 -> [3, 19]
    @staticmethod
    def primeComponents(n):
        def isPrime(m):
            d = 2
            for i in range(2, m):
                if m % i == 0: d += 1
            return d == 2
        
        primes = []
        ns = []

        for i in range(2, n):
            if isPrime(i): primes.append(i)

        ns = itertools.product(*[primes, primes])

        for i in ns:
            if i[0] + i[1] == n: return [i[0], i[1]]
        return []


    # Sprawdzenie czy liczba jest wesoła
    @staticmethod
    def isHappy(n):
        m = list(str(n))
        o = 0
        g = []
        while o is not n:
            if o == n: return False
            for i in m:
                i = int(i)
                o += i ** 2
            if o in g: return False
            if o == 1: return True
            g.append(o)
            m = list(str(o))
            o = 0


    # Rozkład liczby na czynniki pierwsze
    @staticmethod
    def factors(n):
        f = []
        k = 2
        while n > 1:
            if n % k == 0:
                n = n / k
                f.append(k)
            else: k += 1
        return f


    # Sito Eratostenesa - wyznacza zbiór liczb pierwszych z zakresu <2, n>
    @staticmethod
    def sieve(n):
        m = [True for i in range(n + 1)]
        b = []
        p = 2
        while (p ** 2 <= n):
            if (m[p]):
                for i in range(p ** 2, n + 1, p):
                    m[i] = False
            p += 1
        for p in range(2, n + 1):
            if m[p]: b.append(p)
        return b


    # Sprawdzenie czy liczba jest pierwsza
    @staticmethod
    def isPrime(n):
        d = 1
        for i in range(1, n):
            if n % i == 0:
                d += 1
        return d == 2


    # Sprawdzenie czy liczba jest doskonała
    @staticmethod
    def isPerfect(n):
        d = [1]
        for i in range(2, round(n / 2) + 1):
            if n % i == 0: d.append(i)
        return sum(d) == n
    
    
    # Odwracanie tablicy dwuwymiarowej o 90 stopni (traktowanie kolumn jako wierszy)
    # np. 
    # [ [1,2,3], [4,5,6] ] -> [ [1,4], [2,5], [3,6] ]
    #
    #   1 2 3
    #   4 5 6
    #     ||
    #     \/
    #    1 4
    #    2 5
    #    3 6
    #
    @staticmethod
    def columnsAsRows(seq):
        l = len(seq[0])
        i = 0
        d = []
        while i < l:
            t = []
            for j in seq:
                t.append(j[i])
            d.append(t)
            i += 1
        return d

    
    # NWD (największy wspólny dzielnik) metodą dzielenia z resztą
    @staticmethod
    def NWD(a, b):
        while b > 0:
            c = a % b
            a = b
            b = c
        return a


    # NWW (najmniejsza wspólna wielokrotność) z dwóch liczb
    @staticmethod
    def NWW(a, b):
        def NWD(a, b):
            while b > 0:
                c = a % b
                a = b
                b = c
            return a
        return (a * b) / NWD(a, b)

    # Sprawdzenie czy dwie liczby pierwsze są bliźniacze
    @staticmethod
    def areTwins(a, b):
        def isPrime(n):
            d = 1
            for i in range(1, n):
                if n % i == 0:
                    d += 1
            return d == 2
        return isPrime(a) and isPrime(b) and abs(b - a) == 2


    # Szyfrowanie szyfrem cezara operujące na literach angielskich (kody ASCII od 65 do 90)
    # a - słowo
    # k - przesunięcie w prawo
    @staticmethod
    def cesar(a, k):
        n = k // 26
        k -= n * 26
        c = ''
        for i in range(len(a)):
            if ord(a[i]) > 90 - k:
                c += chr(ord(a[i]) + k - 26)
            else:
                c += chr(ord(a[i]) + k)
        return c


    # Odszyfrowanie szyfru cezara operujące na literach angielskich (kody ASCII od 65 do 90)
    # a - słowo
    # k - przesunięcie w lewo
    @staticmethod
    def decesar(a, k):
        w = ''
        k %= 26
        for i in a:
            if ord(i) - k < 65:
                w += chr(ord(i) - k + 26)
            else:
                w += chr(ord(i) - k)
        return w


    # Sprawdzenie czy ciąg liczb jest ciągiem arytmetycznym (minimum dwie liczby)
    # [1, 3, 5, 7] -> True
    # [2, 5, 6, 11] -> False
    @staticmethod
    def isArithmeticSeq(seq):
        r = seq[1] - seq[0]
        i = 0
        while i < len(seq) - 1:
            if seq[i + 1] - seq[i] != r:
                return False
            i += 1
        return True


    # Tworzenie ciągu arytmetycznego jako tablicy
    # a1 - pierwszy wyraz ciągu
    # r - różnica ciągu
    # n - liczba wyrazów ciągu
    @staticmethod
    def createArithmeticSeq(a1, r, n):
        d = []
        while n > 0:
            d.append(a1)
            a1 += r
            n -= 1
        return d


    # Obliczanie miejsc zerowych funkcji kwadratowej - zwraca tablicę
    # a - liczba przy x^2
    # b - liczba przy x
    # c - wyraz wolny
    @staticmethod
    def quadraticFunctionRoots(a, b, c):
        x = []
        d = (b ** 2) - (4 * a * c)
        if d == 0:
            x.append(-b / 2 * a)
        elif d > 0:
            x.append((-b - math.sqrt(d)) / (2 * a))
            x.append((-b + math.sqrt(d)) / (2 * a))
        return x

    # Obliczanie delty funkcji kwadratowej
    # a - liczba przy x^2
    # b - liczba przy x
    # c - wyraz wolny
    @staticmethod
    def delta(a, b, c):
        return (b ** 2) - (4 * a * c)

    
    # Sprawdzanie czy można ułożyć trójkąt z podanych boków
    # a, b, c - dodatnie boki trójkąta
    @staticmethod
    def isTriangle(a, b, c):
        d = [a, b, c]
        d.sort()
        return d[0] + d[1] > d[2]


    # Obliczanie wartości wielomianu schematem Hornera - rekurencyjnie
    # coe - współczynniki jako tablica
    # d - stopień wielomianu
    # x - argument
    @staticmethod
    def hornerRecursive(coe, d, x):
        if d == 0:
            return coe[0]
        return x * Mathx2.hornerRecursive(coe, d - 1, x) + coe[d]


    # Obliczanie wartości wielomianu schematem Hornera - iteracyjnie
    # coe - współczynniki jako tablica
    # d - stopień wielomianu
    # x - argument
    @staticmethod
    def horner(coe, d, x):
        r = coe[0]
        for i in range(1, d + 1):
            r = (r * x) + coe[i]
        return r

    # Silnia - rekurencyjnie
    @staticmethod
    def factorialRecursive(n):
        if n == 0:
            return 1
        else:
            return n * Mathx2.factorialRecursive(n - 1)

    # Różnica zbiorów np. [1,2,5] - [1,3,4] = [2,5]
    @staticmethod
    def diff(a, b):
        s = []
        for i in a:
            if i not in b:
                s.append(i)
        return s

    # Suma zbiorów
    @staticmethod
    def listSum(a, b):
        return list(set(a + b))

    # Iloczyn zbiorów (część wspólna zbiorów)
    @staticmethod
    def listProduct(a, b):
        s = []
        for i in a:
            if i in b:
                s.append(i)
        for i in b:
            if i in a:
                s.append(i)
        return list(set(s))

    # Wariancja zbioru liczb
    @staticmethod
    def variance(nums):
       avg = sum(nums) / len(nums)
       uni = list(set(nums))
       vals = []
       for i in uni:
           c = nums.count(i)
           n = ((i - avg) ** 2) * c
           vals.append(n)
       s = sum(vals)
       return s / len(nums)

    # Odchylenie standardowe
    @staticmethod
    def standardDeviation(nums):
       avg = sum(nums) / len(nums)
       uni = list(set(nums))
       vals = []
       for i in uni:
           c = nums.count(i)
           n = ((i - avg) ** 2) * c
           vals.append(n)
       s = sum(vals)
       return (s / len(nums)) ** 0.5

    # Mediana zbioru liczb
    @staticmethod
    def median(nums):
        nums.sort()
        if len(nums) % 2 == 1:
            return nums[int(len(nums) / 2)]
        else:
            return (nums[int(len(nums) / 2)] + nums[int(len(nums) / 2) - 1]) / 2
    
    # Rozstęp (różnica między największą i najmniejszą wartością)
    @staticmethod
    def ran(nums):
        return max(nums) - min(nums)

    # Moda, dominanta (najczęściej występujący element)
    def mode(els):
        if len(els) == 0: return None
        if [els[0]] * len(els) == els: return els[0]
        c = 0
        num = els[0]
        lens = []
        for i in els:
            f = els.count(i)
            lens.append(f)
            if(f > c):
                c = f
                num = i
        if [lens[0]] * len(lens) == lens: return None
        return num

# print(Mathx2.isAnagram('sram', 'mars'), Mathx2.isAnagram('bark', 'krab'), Mathx2.isAnagram('krab', 'barb'), Mathx2.isAnagram('add', 'asd'))
# print(Mathx2.isPalindrome('sram', 'mars'))
# print(Mathx2.fibRecursive(1), Mathx2.fibRecursive(6))
# print(Mathx2.fib(1), Mathx2.fib(6))
# print(Mathx2.primeComponents(24), Mathx2.primeComponents(22))
# print(Mathx2.isHappy(7), Mathx2.isHappy(85))
# print(Mathx2.factors(100))
# print(Mathx2.sieve(100))
# print(Mathx2.isPrime(7), Mathx2.isPrime(401), Mathx2.isPrime(1))
# print(Mathx2.isPerfect(6), Mathx2.isPerfect(28), Mathx2.isPerfect(145))
# print(Mathx2.columnsAsRows( [ [1,2,3], [4,5,6] ] ))
# print(Mathx2.NWD(282, 78), Mathx2.NWD(14, 26))
# print(Mathx2.NWW(42, 56), Mathx2.NWW(56, 42), Mathx2.NWW(192, 348))
# print(Mathx2.areTwins(3, 5), Mathx2.areTwins(7, 5), Mathx2.areTwins(13, 15))
# print(Mathx2.cesar('INTERPRETOWANIE', 107) == 'LQWHUSUHWRZDQLH', Mathx2.cesar('ROZSZERZANIE', 107) == 'URCVCHUCDQLH')
# print(Mathx2.decesar('ZORO', 14) == 'LADA', Mathx2.decesar('BCYKUNCM', 1718) == 'ZAWISLAK')
# print(Mathx2.isArithmeticSeq([1, 3, 5, 7]), Mathx2.isArithmeticSeq([2, 5, 6, 11]), Mathx2.isArithmeticSeq([12, 12, 12, 12, 12, 12, 12, 12, 12]), Mathx2.isArithmeticSeq([100, 50, 0, -51]))
# print(Mathx2.createArithmeticSeq(1, 2, 5), Mathx2.createArithmeticSeq(3, 0, 10))
# print(Mathx2.quadraticFunctionRoots(1, 2, -3), Mathx2.quadraticFunctionRoots(2, 8, -10), Mathx2.quadraticFunctionRoots(-1, 2, 3))
# print(Mathx2.delta(2, 8, -10))
# print(Mathx2.isTriangle(3, 4, 5), Mathx2.isTriangle(5, 4, 3), Mathx2.isTriangle(4, 4, 8), Mathx2.isTriangle(8,3,4))
# print(Mathx2.hornerRecursive([14, 22, 32, 42, 66], 4, 3))
# print(Mathx2.horner([14, 22, 32, 42, 66], 4, 3))
# print(Mathx2.factorialRecursive(0), Mathx2.factorialRecursive(1), Mathx2.factorialRecursive(6))
# print(Mathx2.diff([1, 2, 5], [1, 3, 4]))
# print(Mathx2.listSum([1, 2, 5], [1, 3, 4]))
# print(Mathx2.listProduct([1, 2, 5], [1, 3, 4]))
# print(Mathx2.variance( [1,2,2,5,2,4,6,11,11,12,1,2,4,6,6,14,13] ), Mathx2.variance( [1,2,3,4,5,6,7,8,9,10,10] ))
# print(Mathx2.standardDeviation( [1,2,2,5,2,4,6,11,11,12,1,2,4,6,6,14,13] ), Mathx2.standardDeviation( [1,2,3,4,5,6,7,8,9,10,10] ))
# print(Mathx2.median( [9, 10, 12, 13, 13, 13, 15, 15, 16, 16, 18, 22, 23, 24, 24, 25] ) == 15.5, Mathx2.median( [1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 5, 5, 6, 7, 7, 7, 7, 9, 9, 9, 45, 45, 47, 47, 120] ) == 5, Mathx2.median([555]) == 555)
# print(Mathx2.ran( [3,5,8,5,5,5,7,9,9,4,22,54,56,7,101,4] ) == 98)
# print(Mathx2.mode( [2,6,2,3,3,6,4,4,6] ) == 6, Mathx2.mode( [-5] ) == -5, Mathx2.mode( [77,2,2,6,6,77] ) == None)