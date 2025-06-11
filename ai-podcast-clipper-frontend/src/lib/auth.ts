import { hash, compare } from 'bcryptjs';

export async function hashPassword(password: string) {

    return hash(password, 10);
}

export async function comparePasswords(plainPassword: string, hashedPassword: string) {
    return compare(plainPassword, hashedPassword);
}