import { Routes } from '@angular/router';
import { InvoiceComponent } from './invoice/invoice.component';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';



export const routes: Routes = [
    { path: '', redirectTo: '/login', pathMatch: 'full'},
    { path: 'invoice', component: InvoiceComponent },
    { path: 'login', component: AppComponent },
    { path: 'register', component: AppComponent },
    { path: 'login', component: LoginComponent },
    { path: 'register', component: RegisterComponent },
];