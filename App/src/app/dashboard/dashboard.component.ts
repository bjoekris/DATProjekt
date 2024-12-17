import { Component } from '@angular/core';

@Component({
  selector: 'app-dashboard',
  imports: [],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent {
  loggedInUser: any;

  ngOnInit() {
    this.loggedInUser = JSON.parse(localStorage.getItem('loggedInUser') || '{}');
  }
}
