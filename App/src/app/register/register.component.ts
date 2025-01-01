import { Component } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../auth.service';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-register',
  standalone: true,
  imports: [FormsModule, RouterModule, CommonModule],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {
  email: string = '';
  password: string = '';
  confirmPassword: string = '';
  errorMessage: string = '';

  constructor(private authService: AuthService, private router:Router) {}

  onRegister() {
    this.authService.register(this.email, this.password).subscribe(
      (response) => {
        console.log('Registration succesful', response);
        this.router.navigate(['/login']);
      },
      (error) => {
        console.error('Registration failed', error);
        this.errorMessage = error.error.message || 'Registration failed';
      }
    );
  }
}
