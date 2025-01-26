import { Component, Input } from '@angular/core';
import {CdkAccordionModule} from '@angular/cdk/accordion';

@Component({
  selector: 'app-type-info',
  imports: [CdkAccordionModule],
  templateUrl: './type-info.component.html',
  styleUrl: './type-info.component.css'
})
export class TypeInfoComponent {
  @Input() items: { title: string, description: string }[] = [];
  expandedIndex = 0;
}
