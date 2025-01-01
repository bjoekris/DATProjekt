// import { Component } from '@angular/core';
// import { Router, RouterModule } from '@angular/router';
// import { FormsModule } from '@angular/forms';
// import { AuthService } from '../auth.service';


// @Component({
//   selector: 'app-login',
//   standalone: true,
//   imports: [FormsModule, RouterModule],
//   templateUrl: './login.component.html',
//   styleUrls: ['./login.component.css'],
// })
// export class LoginComponent {
//   email: string = '';
//   password: string = '';

//   constructor(private authService: AuthService, private router: Router) {}

//   onLogin() {
//     this.authService.login(this.email, this.password).subscribe(
//       (response) => {
//         console.log('Login succesful', response);

//         //naviger til:
//         this.router.navigate(['/invoice']);
//       },
//       (error) => {
//         console.error('Login failed', error);
//       }
//     );
//   }
// }

import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../auth.service';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';


@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, RouterModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent {
  email: string = '';
  password: string = '';

  constructor(private authService: AuthService, private router: Router) {}

  onLogin() {
    this.authService.login(this.email, this.password).subscribe(
      (response) => {
        console.log('Login successful', response);
        this.router.navigate(['/invoice']); // Navigate to /invoice after successful login
      },
      (error) => {
        console.error('Login failed', error);
      }
    );
  }
}

