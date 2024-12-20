import { Component } from '@angular/core';
import { AuthService } from './auth.service';
import { FormsModule } from '@angular/forms'; 


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'App';
  username: string = '';
  password: string = '';
  message: string = '';

  constructor(private authService: AuthService) {}

  //Login
  login() {
    this.authService.login(this.username, this.password).subscribe({
      next: (response: any) => {
        console.log('Login succesful:', response);
        this.message = 'Login succesful Token: ' + response.token;
      },
      error: (error: any) => {
        console.error('Login failed:', error);
        this.message = 'Login failed';
      }
    });
  }

  //Registrer
  register() {
    this.authService.register(this.username, this.password).subscribe({
      next: (response) => {
        console.log('Register succesful:', response);
        this.message = 'Register succesful';
      },
      error: (error) => {
        console.error('Register failed:', error);
        this.message = 'Register failed';
      }
    });
  }
  
}
