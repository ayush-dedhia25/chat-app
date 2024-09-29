import { TOKEN_KEY } from "../constants";

export const encryptData = async (data, key) => {
  const encodedData = new TextEncoder().encode(JSON.stringify(data));

  // Create a random initialization vector (IV) for each encryption
  const iv = window.crypto.getRandomValues(new Uint8Array(12));

  // Encrypt the data
  const encryptedData = await window.crypto.subtle.encrypt(
    { name: "AES-GCM", iv },
    key,
    encodedData
  );

  // Return the IV and encrypted data (both needed for decryption)
  return {
    iv: Array.from(iv),
    cipherText: Array.from(new Uint8Array(encryptedData)),
  };
};

export const decryptData = async (encryptedData, key) => {
  const { iv, cipherText } = encryptedData;
  const ivBufferArray = new Uint8Array(iv);
  const cipherTextBufferArray = new Uint8Array(cipherText);

  // Decrypt the data
  const decryptedData = await window.crypto.subtle.decrypt(
    { name: "AES-GCM", iv: ivBufferArray },
    key,
    cipherTextBufferArray
  );

  // Return the decrypted data as a string
  return JSON.parse(new TextDecoder().decode(decryptedData));
};

export const generateEncryptionKey = async () => {
  return window.crypto.subtle.generateKey({ name: "AES-GCM", length: 256 }, true, [
    "encrypt",
    "decrypt",
  ]);
};

export const generateAndStoreKey = async () => {
  if (!sessionStorage.getItem("encryptionKey")) {
    const key = await generateEncryptionKey();
    const exportedKey = await window.crypto.subtle.exportKey("jwk", key);
    sessionStorage.setItem("encryptionKey", JSON.stringify(exportedKey));
    return key;
  } else {
    const storedKey = JSON.parse(sessionStorage.getItem("encryptionKey"));
    return window.crypto.subtle.importKey("jwk", storedKey, { name: "AES-GCM" }, true, [
      "encrypt",
      "decrypt",
    ]);
  }
};

export const retrieveDecryptedToken = async () => {
  const key = await generateAndStoreKey(); // Retrieve the encryption key
  const encryptedToken = JSON.parse(localStorage.getItem(TOKEN_KEY)); // Get the encrypted token from localStorage

  if (encryptedToken) {
    const decryptedToken = await decryptData(encryptedToken, key); // Decrypt the token
    return decryptedToken;
  }
  return null;
};
