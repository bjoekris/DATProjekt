import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

import { saveAs } from 'file-saver';
import { TemplateService } from './template.service';
import mammoth from 'mammoth';

interface DynamicField {
  name: string;
  type: 'text' | 'number' | 'file' | 'media' | 'list' | 'image';
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule], 
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers: [HttpClient]
})
export class AppComponent {
  templateFile: File | null = null;
  formData: any = {};
  dynamicFields: DynamicField[] = [];
  listFields: { name: string, type: DynamicField['type'] }[] = [];
  title = 'App';

  constructor(private templateService: TemplateService, private http: HttpClient) {}

  async onFileChange(event: any): Promise<void> {
    this.templateFile = event.target.files[0];
    console.log("OnFileChange function called");
    const file = event.target.files[0];

    try {
      const arrayBuffer = await file.arrayBuffer();
      const result = await mammoth.extractRawText({ arrayBuffer });
      const text = result.value;

      const forBlocks: { start: number, end: number, variable: string, type: DynamicField['type'] }[] = [];
      const forRegex = /{% for (\w+) in (\w+) %}/g;
      let match;
      while ((match = forRegex.exec(text)) !== null) {
        const start = match.index;
        const endforRegex = /{% endfor %}/g;
        endforRegex.lastIndex = forRegex.lastIndex;
        const endMatch = endforRegex.exec(text);
        if (endMatch) {
          const end = endMatch.index + endMatch[0].length;
          let type: DynamicField['type'] = 'list';
          if (match[2].toLowerCase().includes('image')) {
            type = 'image';
          } else {
            type = 'list';
          }
          forBlocks.push({ start, end, variable: match[2], type });
        }
      }

      const regex = /{{([^}]+)}}/g;
      const matches = text.matchAll(regex);

      this.dynamicFields = [];
      this.listFields = [];

      for (const match of matches) {
        const variable = match[1].trim();

        let type: DynamicField['type'] = 'text';
        if (variable.endsWith('_text')) {
          type = 'text';
        } else if (variable.endsWith('_number')) {
          type = 'number';
        } else if (variable.endsWith('_file')) {
          type = 'file';
        } else if (variable.endsWith('media')) {
          type = 'media';
        }

        const name = variable.replace(/(?:text|number|file|media)$/, '');

        let isList = false;
        for (const block of forBlocks) {
          if (match.index >= block.start && match.index < block.end) {
            this.listFields.push({ name: block.variable, type: block.type });
            isList = true;
            break;
          }
        }

        if (!isList) {
          this.dynamicFields.push({ name, type });
        }
      }

      console.log("DynamicFields:", this.dynamicFields);
      console.log("ListFields:", this.listFields);

    } catch (error) {
      console.error("Error processing DOCX file:", error);
    }
  }

  onSubmit() {
    console.log("OnSubmit function called");
    if (!this.templateFile) {
      alert('Please upload a template file.');
      return;
    }

    const apiKey = 'abc123456789';
    this.templateService.sendDynamicData(this.templateFile, this.formData, apiKey)
      .subscribe(response => {
        saveAs(response, 'generated.pdf');
      }, error => {
        console.error('Error generating PDF:', error);
      });
  }

  trackByIndex(index: number, item: any): any {
    return index;
  }

  addListItem(listFieldName: string): void {
    if (!this.formData[listFieldName]) {
      this.formData[listFieldName] = [];
    }
    this.formData[listFieldName].push('');
  }

  removeListItem(listFieldName: string, index: number): void {
    if (this.formData[listFieldName]) {
      this.formData[listFieldName].splice(index, 1);
    }
  }
}