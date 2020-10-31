import random, math

# Поиск простого числа 
def find_prime(NumBits, NumRounds):
    p = 0
    while(1):
        n = random.randrange(2 ** NumBits // 2, 2 ** NumBits*4 // 2) * 2 + 1
        if isPrime(n, NumRounds) == True: 
            p = n
            break
        else:
            continue
    return p

# Проверка простоты числа тестом Миллера-Рабина
def isPrime(n, NumRounds=32):
    if n < 2: return False
    s = i = 0
    d = n-1
    while d % 2 == 0:
        s += 1
        d = d//2
    while (i < (NumRounds)):
        i += 1
        x = pow(random.randint(2,n-1), d, n)
        if x == 1 or x == n-1: continue
        for r in range(1, s):
            x = (x * x) % n
            if x == 1: return False
            if x == n-1: break
        else: return False
    return True

# Поиск первообразного корня
def find_primitive_root(p):
		if p == 2: return 1
		p1 = 2
		p2 = (p-1) // p1
		while(1):
			g = random.randint( 2, p-1 )
			if not (pow(g, (p-1)//p1, p) == 1):
			    if not pow(g, (p-1)//p2, p) == 1:
				    return g

# Генерация ключей
def generate_keys(NumBits=32, NumRounds=20):
    p = find_prime(NumBits, NumRounds)
    g = find_primitive_root(p)
    g = pow(g, 2, p)
    x = random.randint(1, (p - 1) // 2)
    y = pow(g, x, p)
    return {'Prime':p, 'Root':g, 'Private':x, 'Public':y}

# Шифрование 
def encrypt(y, p, g, M):
	k = random.randint(1, p)
	a = pow(g, k, p)
	cipher_text = ""
	cipher = []
	
	for i in M:
		b = (ord(i)*pow(y, k, p)) % p 
		cipher.append(b)
	
	for j in cipher:
		cipher_text += str(j) + ' '
	cipher_text = cipher_text[:-1] 
	return {'a':a, 'b':cipher_text} 

def decrypt(x, p, g, a, cipher):
    text = ''
    for i in cipher.split(" "):
        s = pow(a, x, p)
        text += chr((int(i)*pow(s, p-2, p)) % p)
    return text

NumBits = int(input("Укажите размерность ключа: "))
data = generate_keys(NumBits)
priv = data['Private']
pub = data['Public']
prime = data['Prime']
root = data['Root']
print('\n',data, '\n')
text = str(input("Введите текст: "))	
# text = "French text:  Maître Corbeau. Chinese text: 鋈 晛桼桾 枲柊氠 藶藽. Russian text: Некуда жить, вот и думаешь в голову!"
cipherpair = encrypt(pub, prime, root, text)
print('\nШифротекст:\n' + cipherpair['b'])	
decrypted_text = decrypt(priv, prime, root, cipherpair['a'], cipherpair['b'])
print('\nРасшифрованный текст:\n' + decrypted_text)