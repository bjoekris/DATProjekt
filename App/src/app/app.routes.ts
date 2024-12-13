import { Routes } from '@angular/router';
import { InvoiceComponent } from './invoice/invoice.component';


export const routes: Routes = [
    { path: '', redirectTo: '/invoice', pathMatch: 'full'},
    { path: 'invoice', component: InvoiceComponent }
];