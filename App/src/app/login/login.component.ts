import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  imports: [FormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  email: string = '';
  password: string = '';

  constructor(private router: Router) {}

  onSubmit() {
    const users = JSON.parse(localStorage.getItem('users') || '[]');

    const user = users.find(
      (u:any) => u.email === this.email && u.password === this.password
    );

    if (user) {
      alert('Login successful');

      localStorage.setItem('loggedInUser', JSON.stringify(user));

      this.router.navigate(['/dashboard']);
    } else {
      alert('Invalid credentials');
    }
  }
}
