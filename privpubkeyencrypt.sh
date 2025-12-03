# Generate a 2048-bit private key
openssl genrsa -out private.pem 2048

# Extract the public key
openssl rsa -in private.pem -pubout -out public.pem

echo "Hello, this is a secret message!" > message.txt

#Encrypt with pub key
openssl pkeyutl -encrypt -inkey public.pem -pubin -in message.txt -out encrypted_pub.bin

#Decrypt with private key
openssl pkeyutl -decrypt -inkey private.pem -in encrypted_pub.bin -out decrypted_pub.txt



#Encrypt with private Key
openssl pkeyutl -sign -inkey private.pem -in message.txt -out encrypted.bin
#Decrypt with public key
openssl pkeyutl -verify -inkey public.pem -pubin -in message.txt -sigfile encrypted.bin

