import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {
  email: string='';
  password: string='';

  onSubmit() {
    const users = JSON.parse(localStorage.getItem('users') || '[]');

    const userExists = users.some((u:any) => u.email === this.email);

    if (userExists) {
      alert('User already exists');
    } else {
      users.push({ email: this.email, password: this.password });

      localStorage.setItem('users', JSON.stringify(users));

      alert('User registered successfully');
    }
  }
}
