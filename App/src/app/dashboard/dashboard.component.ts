import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule, HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, HttpClientModule], // Add HttpClientModule here
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent {
  loggedInUser: any;

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.loggedInUser = JSON.parse(localStorage.getItem('loggedInUser') || '{}');
  }
}