import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root',
})
export class AuthService {
    private baseUrl = 'http://localhost:3000';

    constructor(private http: HttpClient) {}
    // constructor(private http: HttpClient) {
    //     console.log('HttpClient injected:', this.http);
    //   }
      

    login(username: string, password: string): Observable<any> {
        return this.http.post(`${this.baseUrl}/login`, { username, password });
    }

    register(username: string, password: string): Observable<any> {
        return this.http.post(`${this.baseUrl}/register`, { username, password });
    }
}


// registerUser(user: { username: string; password: string }): Observable<any> {
//     return this.http.post(`${this.baseUrl}/register`, user);
// }

// loginUser(user: { username: string; password: string }): Observable<any> {
//     return this.http.post(`${this.baseUrl}/login`, user);
// }