import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { InvoiceComponent } from './invoice/invoice.component';
import { AuthGuard } from './auth.guard';
import { ConverterComponent } from './converter/converter.component';


export const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'invoice', component: InvoiceComponent, canActivate: [AuthGuard] },
  { path: 'converter', component: ConverterComponent }, 
  { path: '**', redirectTo: '/login' },
];