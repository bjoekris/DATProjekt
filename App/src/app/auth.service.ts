import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root',
})
export class AuthService {
    private baseUrl = 'http://localhost:3000';
    private tokenKey = 'token';

    constructor(private http: HttpClient) {}

    login(email: string, password: string): Observable<any> {
        return this.http.post(`${this.baseUrl}/login`, { email, password });
    }

    register(email: string, password: string): Observable<any> {
        return this.http.post(`${this.baseUrl}/register`, { email, password });
    }

    isLoggedIn(): boolean {
        if (typeof window !== 'undefined' && localStorage) {
            return !!localStorage.getItem(this.tokenKey);
        }
        return false;
    }

    saveToken(token: string): void {
        localStorage.setItem(this.tokenKey, token);
    }

    logout(): void {
        localStorage.removeItem(this.tokenKey);
        console.log('Logged out');
    }


}