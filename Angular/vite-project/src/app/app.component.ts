import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

import { saveAs } from 'file-saver';
import { TemplateService } from './template.service';
import mammoth from 'mammoth';

//Bjørn

interface DynamicField {
  name: string;
  type: 'text' | 'number' | 'file' | 'media' | 'list' | 'image' | 'table';
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
  formData: any = {
    Images: []
  };
  dynamicFields: DynamicField[] = [];
  loading: boolean = false;
  listFields: { name: string, variables?: Map<string, string[]>, type: DynamicField['type'] }[] = [];
  tableFields: { name: string, objectRef: string, variables: Map<string, string[]>, type: DynamicField['type'] }[] = [];
  title = 'App';

  constructor(private templateService: TemplateService, private http: HttpClient) {}


  async onFileChange(event: any): Promise<void> {
    this.loading = true;
    this.templateFile = event.target.files[0];
    console.log("OnFileChange function called");
   
    //Check if file exists
    if (!this.templateFile) {
      return;
    }

    const file = event.target.files[0];

    const listFields: string[] = [];
    const tableFields: string[] = [];

    try {
      const arrayBuffer = await this.templateFile.arrayBuffer();
      const result = await mammoth.extractRawText({ arrayBuffer });
      const text = result.value;
    
      // Used to identify lists and their variables
      const listForRegex = /{% for (\w+) in (\w+) %}/g;
      let match;
      while ((match = listForRegex.exec(text)) !== null) {
        const listEndforRegex = /{% endfor %}/g;
        listEndforRegex.lastIndex = listForRegex.lastIndex;
        const endMatch = listEndforRegex.exec(text);
        if (endMatch) {
          let type: DynamicField['type'] = 'list';
          if (match[2].toLowerCase().includes('image')) {
            type = 'image';
          } else {
            type = 'list';
          }
          this.listFields.push({ name: match[2], type });
          listFields.push(match[1]);
        }
      }
    
      // Used to identify tables and their variables
      const tableVariables = new Map<string, string[]>();
      const tableForRegex = /{%[tc]r for (\w+) in (\w+) %}/g;
      const objectReference = '';
      const variables = [];
      let tableName = '';
      while ((match = tableForRegex.exec(text)) !== null) {
        const objectReference = match[1];
        tableName = match[2];
        if (!this.formData[tableName]) {
          this.formData[tableName] = [tableName];
        }
        const tableStart = match.index;
        const tableEndforRegex = /{% endfor %}/g;
        tableEndforRegex.lastIndex = tableForRegex.lastIndex;
        const tableEndMatch = tableEndforRegex.exec(text);
        if (tableEndMatch) {
          const tableEnd = tableEndMatch.index + tableEndMatch[0].length;
          const variableRegex = new RegExp(`{{${objectReference}\\.([^}]+)}}`, 'g');
          let variableMatch;
          while ((variableMatch = variableRegex.exec(text.substring(tableStart, tableEnd))) !== null) {
            const variableName = variableMatch[1];
            variables.push(variableName);
            tableFields.push(objectReference+"."+variableName);
          }
        }
      }
      tableVariables.set(objectReference, variables);
      this.tableFields.push({ name: tableName, objectRef: objectReference, variables: tableVariables, type: 'table' });

      // Used in the table display
      if (!this.formData[tableName]) {
        this.formData[tableName] = [{}];
        variables.forEach(variable => {
          this.formData[tableName][0][variable] = '';
        });
      }
    
      const regex = /{{([^}]+)}}/g;
      const matches = text.matchAll(regex);
    
      for (const match of matches) {
        const variable = match[1].trim();
        
        let type: DynamicField['type'] = 'text';
        if (variable.endsWith('_text')) {
          type = 'text';
        } else if (variable.endsWith('number')) {
          type = 'number';
        } else if (variable.endsWith('file')) {
          type = 'file';
        } else if (variable.endsWith('media')) {
          type = 'media';
        }
    
        const name = variable.replace(/(?:text|number|file|media)$/, '');
        
        if (listFields.includes(variable) || tableFields.includes(variable) || variable.toLowerCase().includes('image')) {
          continue;
        }
  
        this.dynamicFields.push({ name, type });
      }
    
      console.log("DynamicFields:", this.dynamicFields);
      console.log("ListFields:", this.listFields);
      console.log("TableFields:", this.tableFields);
    
      this.loading = false;
    } catch (error) {
      console.error("Error processing WORD file:", error);
      this.loading = false;
    }
  }

  onSubmit() {
    this.loading = true;
    console.log("OnSubmit function called");
    if (!this.templateFile) {
      alert('Upload venligst en skabelonfil.');
      return;
    }

    const apiKey = '123456789';
    this.templateService.sendDynamicData(this.templateFile, this.formData, apiKey)
      .subscribe(response => {
        saveAs(response, 'invoiEZ.pdf');
        this.loading = false;
      }, error => {
        console.error('Error generating PDF:', error);
        this.loading = false;
      });
  }

  trackByIndex(index: number, item: any): any {
    return index;
  }

  addListItem(listFieldName: string): void {
    if (!this.formData[listFieldName]) {
      this.formData[listFieldName] = [];
    }
    if (listFieldName.toLowerCase().includes('image')) {
      this.formData[listFieldName].push({ URL: '', Size: 100, List: 1, Option: 'Auto' });
    } else {
      this.formData[listFieldName].push('');
    }
  }

  removeListItem(listFieldName: string, index: number): void {
    if (this.formData[listFieldName]) {
      this.formData[listFieldName].splice(index, 1);
    }
  }

  addTableRow(tableName: string, columns: string[]): void {
    if (!this.formData[tableName]) {
      this.formData[tableName] = [];
    }
    
    for (let element of this.formData[tableName]) {
      if (element === tableName) {
        element = [];
      }
    }

    const newRow: any = {};
    columns.forEach(column => {
      newRow[column] = '';
    });
    this.formData[tableName].push(newRow);
  }

  removeTableRow(tableName: string, index: number): void {
    if (this.formData[tableName]) {
      this.formData[tableName].splice(index, 1);
    }
  }
}