import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../auth.service';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, RouterModule, CommonModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent {
  email: string = '';
  password: string = '';
  errorMessage: string = '';

  constructor(private authService: AuthService, private router: Router) {}

  onLogin() {
    this.errorMessage = '';
  
    this.authService.login(this.email, this.password).subscribe({
      next: (response) => {
        console.log('Login successful', response);
        this.authService.saveToken(response.token);
        this.router.navigate(['/invoice']);
      },
      error: (error) => {
        console.error('Login failed', error);
        this.errorMessage = error.error.message || 'Login failed';
      }
    });
  }
  
}
