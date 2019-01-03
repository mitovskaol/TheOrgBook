import { Inject, LOCALE_ID, Pipe, PipeTransform } from '@angular/core';
import { DatePipe } from '@angular/common';
import { AppConfigService } from '../app-config.service';

@Pipe({
  name: 'dateFormat',
  pure: true
})
export class DateFormatPipe extends DatePipe implements PipeTransform {
  constructor(
      @Inject(LOCALE_ID) private _locale: string,
      private _config: AppConfigService) {
    super(_locale);
  }

  transform(value: any, args?: any): any {
    let format = arguments[1] || 'mediumDate';
    let timezone = arguments[2] || this._config.getConfig().DISPLAY_TIMEZONE || undefined;
    if(format === 'effectiveDate') format = 'mediumDate';
    else if(format === 'effectiveDateTime') format = 'MMM d, y, h:mm a';
    if(value && value.match(/^\d{4}-\d{2}-\d{2}$/)) {
      // prevent date from being shifted forward or backward
      timezone = 'UTC';
    }
    return super.transform(value, format, timezone);
  }
}
