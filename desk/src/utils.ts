import { useClipboard, useDateFormat, useTimeAgo } from "@vueuse/core";
import dayjs from "dayjs";
import { FeatherIcon, toast } from "frappe-ui";
import { gemoji } from "gemoji";
import { h, markRaw, ref } from "vue";
import zod from "zod";
import TicketIcon from "./components/icons/TicketIcon.vue";
/**
 * Wrapper to create toasts, supplied with default options.
 * https://frappeui.com/components/toast.html
 * @param options - `Toast` options
 */

/**
 * Copy a string to clipboard, and create a toast
 * @param s - String to copy
 */
export async function copy(s: string) {
  const { copy: c } = useClipboard();
  c(s).then(() => toast.success("Copied to clipboard"));
}

/**
 * Get assigned user from `_assign` string. The return value is a `string`,
 * not a `User` object.
 * @param s - `_assign` string (JSON)
 * @returns user id
 */
export function getAssign(s: string): string | undefined {
  const assignJson = JSON.parse(s);
  const arr = Array.isArray(assignJson) ? assignJson : [];
  return arr.slice(-1).pop();
}

export function validateEmail(email) {
  const regExp =
    /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return regExp.test(email);
}

export function validateEmailWithZod(email: string) {
  const success = zod.string().email().safeParse(email).success;
  return success;
}

export function dateFormat(date, format) {
  const _format = format || "DD-MM-YYYY HH:mm:ss";
  return useDateFormat(date, _format).value;
}

export function timeAgo(date) {
  return useTimeAgo(date).value;
}

export const dateTooltipFormat = "ddd, MMM D, YYYY h:mm A";

export function errorMessage(title, message) {
  toast.error(message);
}

export function formatTime(seconds) {
  const days = Math.floor(seconds / (3600 * 24));
  const hours = Math.floor((seconds % (3600 * 24)) / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const remainingSeconds = Math.floor(seconds % 60);

  let formattedTime = "";

  if (days > 0) {
    formattedTime += `${days}d `;
  }

  if (hours > 0 || days > 0) {
    formattedTime += `${hours}h `;
  }

  if (minutes > 0 || hours > 0 || days > 0) {
    formattedTime += `${minutes}m `;
  }

  formattedTime += `${
    remainingSeconds >= 10 ? remainingSeconds : "0" + remainingSeconds
  }s`;

  return formattedTime.trim();
}

export function getTimeInSeconds(time: string) {
  // time in the format 1h 2m 3s
  let timeParts = time.split(" ");
  let seconds = 0;
  timeParts.forEach((part) => {
    if (part.endsWith("d")) {
      seconds += parseInt(part) * 24 * 60 * 60; // days
    } else if (part.endsWith("h")) {
      seconds += parseInt(part) * 60 * 60; // hours
    } else if (part.endsWith("m")) {
      seconds += parseInt(part) * 60; // minutes
    } else if (part.endsWith("s")) {
      seconds += parseInt(part); // seconds
    }
  });
  return seconds;
}

export const isCustomerPortal = ref(false);

export async function copyToClipboard(
  msg: string = "",
  toastMessage: string = "Copied to clipboard"
) {
  if (navigator.clipboard && window.isSecureContext) {
    await navigator.clipboard.writeText(msg);
  } else {
    let input = document.createElement("input");
    let body = document.querySelector("body");
    body.appendChild(input);
    input.value = msg;
    input.select();
    document.execCommand("copy");
    input.remove();
  }

  toast.success(toastMessage);
}

export const textEditorMenuButtons = [
  "Paragraph",
  ["Heading 2", "Heading 3", "Heading 4", "Heading 5", "Heading 6"],
  "Separator",
  "Bold",
  "Italic",
  "Separator",
  "Bullet List",
  "Numbered List",
  "Separator",
  "Align Left",
  "Align Center",
  "Align Right",
  "FontColor",
  "Separator",
  "Image",
  "Video",
  "Link",
  "Blockquote",
  "Code",
  "Horizontal Rule",
  [
    "InsertTable",
    "AddColumnBefore",
    "AddColumnAfter",
    "DeleteColumn",
    "AddRowBefore",
    "AddRowAfter",
    "DeleteRow",
    "MergeCells",
    "SplitCell",
    "ToggleHeaderColumn",
    "ToggleHeaderRow",
    "ToggleHeaderCell",
    "DeleteTable",
  ],
];

export function isContentEmpty(content: string) {
  const parser = new DOMParser();
  const doc = parser.parseFromString(content, "text/html");
  return doc.body.textContent === "";
}

export function isTouchScreenDevice() {
  return "ontouchstart" in document.documentElement;
}

export function isEmoji(str) {
  const emojiList = gemoji.map((emoji) => emoji.emoji);
  return emojiList.includes(str);
}

export function getIcon(icon) {
  if (isEmoji(icon)) {
    return h("div", icon);
  }
  return icon || markRaw(TicketIcon);
}
export function formatTimeShort(date: string) {
  const now = dayjs();
  const inputDate = dayjs.tz(date);
  const diffSeconds = now.diff(inputDate, "second");
  const diffMinutes = now.diff(inputDate, "minute");
  const diffHours = now.diff(inputDate, "hour");
  const diffDays = now.diff(inputDate, "day");
  const diffWeeks = now.diff(inputDate, "week");
  const diffMonths = now.diff(inputDate, "month");
  const diffYears = now.diff(inputDate, "year");

  if (diffSeconds < 60) return `${diffSeconds} s`;
  if (diffMinutes < 60) return `${diffMinutes} m`;
  if (diffHours < 24) return `${diffHours} h`;
  if (diffDays < 7) return `${diffDays} d`;
  if (diffWeeks < 4) return `${diffWeeks} w`;
  if (diffMonths < 12) return `${diffMonths} M`;
  return `${diffYears}Y`;
}

function hasArabicContent(content: string) {
  const arabicRegex = /[\u0600-\u06FF]/;
  return arabicRegex.test(content);
}

export function getFontFamily(content: string) {
  const langMap = {
    default: "!font-[InterVar]",
    arabic: "!font-[system-ui]",
  };
  let lang = "default";
  if (hasArabicContent(content)) {
    lang = "arabic";
  }
  return langMap[lang];
}

/**
 * Parses HTML string and returns the text content with preserved line breaks
 * @param html - HTML string to parse
 * @returns Plain text content with preserved line breaks
 */
export function htmlToText(html: string): string {
  if (!html) return "";

  const parser = new DOMParser();
  const doc = parser.parseFromString(html, "text/html");

  const lineBreaks = doc.querySelectorAll("br, p, div, li");
  lineBreaks.forEach((el) => {
    el.after("\n");
  });

  let text = doc.body.textContent || "";

  text = text.replace(/\s+/g, " ");

  text = text.replace(/\n\s*\n/g, "\n");

  return text.trim();
}

/**
 * Format a date according to the user's system settings
 * @param {Date|string} date - Date object or ISO date string
 * @returns {string} Formatted date string in the user's locale and preferences
 */
export function getFormat(date) {
  if (!date) return "";

  const dateObj = date instanceof Date ? date : new Date(date);
  if (isNaN(dateObj.getTime())) return "";

  // Use the browser's default locale and options
  return new Intl.DateTimeFormat(undefined, {
    year: "numeric",
    month: "numeric",
    day: "numeric",
  }).format(dateObj);
}

export function TemplateOption({ active, option, variant, icon, onClick }) {
  return h(
    "button",
    {
      class: [
        active ? "bg-surface-gray-2" : "text-ink-gray-8",
        "group flex w-full gap-2 items-center rounded-md px-2 py-2 text-base",
        variant == "danger" ? "text-ink-red-3 hover:bg-ink-red-1" : "",
      ],
      onClick: onClick,
    },
    [
      icon
        ? h(FeatherIcon, {
            name: icon,
            class: ["h-4 w-4 shrink-0"],
            "aria-hidden": true,
          })
        : null,
      h("span", { class: "whitespace-nowrap" }, option),
    ]
  );
}

export function getGridTemplateColumnsForTable(columns) {
  let columnsWidth = columns
    .map((col) => {
      let width = col.width || 1;
      if (typeof width === "number") {
        return width + "fr";
      }
      return width;
    })
    .join(" ");
  return columnsWidth + " 22px";
}

const OPERATOR_MAP: Record<string, string> = {
  equals: "==",
  "=": "==",
  "!=": "!=",
  "not equals": "!=",
  "<": "<",
  "<=": "<=",
  ">": ">",
  ">=": ">=",
  in: "in",
  "not in": "not in",
  like: "like",
  "not like": "not like",
  is: "is",
  "is not": "is not",
  between: "between",
  timespan: "timespan",
} as const;

interface FieldMetadata {
  fieldname: string;
  fieldtype?: string;
  label?: string;
  options?: string;
}

interface Condition {
  field: FieldMetadata | string;
  operator: string;
  value: unknown;
  conjunction?: "and" | "or";
}

/**
 * Convert conditions object/array to a string representation
 * @param conditions - Single condition or array of conditions
 * @param isNested - Whether this is a nested condition (internal use)
 * @returns String representation of the conditions
 */
export const convertToConditions = (
  conditions: Condition | Condition[] | null,
  isNested = false
): string => {
  if (!conditions) return "";

  const conditionList = Array.isArray(conditions) ? conditions : [conditions];
  const conditionsStr: string[] = [];

  for (const { field, operator = "==", value } of conditionList) {
    if (
      typeof field === "string" &&
      field === "group" &&
      Array.isArray(value)
    ) {
      const nestedCondition = convertToConditions(value, true);
      if (nestedCondition) {
        conditionsStr.push(`(${nestedCondition})`);
      }
      continue;
    }

    if (typeof field !== "object" || !("fieldname" in field)) {
      continue;
    }

    const { fieldname, fieldtype = "" } = field;
    const normalizedOp = operator.toLowerCase();
    const op = OPERATOR_MAP[normalizedOp] || normalizedOp;

    if (op === "timespan") {
      conditionsStr.push(`# Timespan: ${value} not implemented`);
      continue;
    }

    let valueStr = formatValueForCondition(fieldname, fieldtype, op, value);
    if (valueStr === null) continue;

    let conditionStr = `${fieldname} ${op} ${valueStr}`;

    if (
      fieldtype === "Check" &&
      op === "==" &&
      (valueStr === "0" || valueStr === "1")
    ) {
      conditionStr = valueStr === "1" ? fieldname : `not ${fieldname}`;
    }

    conditionsStr.push(conditionStr);
  }

  if (!conditionsStr.length) return "";

  const defaultConjunction = conditionList[0]?.conjunction || "and";
  let result = conditionsStr.join(` ${defaultConjunction} `);

  if (!isNested && conditionList.length === 1 && !/[\(\)]/.test(result)) {
    return result;
  }

  result = result.replace(/\s+/g, " ").trim();
  if (isNested && conditionList.length > 1) {
    result = `(${result})`;
  }

  return result.replace(/\(\s*\(/g, "(").replace(/\)\s*\)/g, ")");
};

/**
 * Format a value for use in a condition string
 * @param fieldname - Name of the field
 * @param fieldtype - Type of the field
 * @param op - Operator being used
 * @param value - Value to format
 * @returns Formatted value string or null if special case was handled
 */
function formatValueForCondition(
  fieldname: string,
  fieldtype: string,
  op: string,
  value: unknown
): string {
  if (value === null || value === undefined) {
    return "None";
  }

  if (typeof value === "string") {
    if (fieldname === "_assign") {
      if (op === "is") return "None";
      if (op === "like" || op === "not like") return `'%${value}%'`;
      return `'${value}'`;
    }

    if (op === "between" && value.includes(",")) {
      const [start, end] = value.split(",").map((v) => v.trim());
      return `'${start}' and '${end}'`;
    }

    if ((op === "in" || op === "not in") && value.includes(",")) {
      const items = value.split(",").map((v) => `'${v.trim()}'`);
      return `[${items.join(", ")}]`;
    }

    if (op === "like" || op === "not like") {
      return `'%${value}%'`;
    }

    if (fieldtype === "Check") {
      const boolValue = ["yes", "true", "1"].includes(value.toLowerCase());
      return boolValue ? "1" : "0";
    }

    return `'${value}'`;
  }

  if (typeof value === "number" || typeof value === "boolean") {
    return String(value).toLowerCase();
  }

  return String(value);
}

interface FieldInfo extends Omit<FieldMetadata, "fieldname"> {
  value: string;
  fieldname: string;
}

// Operator mapping for string to operator conversion
const STRING_TO_OPERATOR: Record<string, string> = {
  "==": "equals",
  "!=": "not equals",
  "<": "<",
  "<=": "<=",
  ">": ">",
  ">=": ">=",
  in: "in",
  "not in": "not in",
} as const;

/**
 * Convert a condition string back to a structured Condition object
 * @param conditionStr - String representation of conditions
 * @param fieldsMeta - Optional metadata about available fields
 * @returns Array of Condition objects
 */
export const convertToObject = (
  conditionStr: string,
  fieldsMeta: Record<string, FieldMetadata> = {}
): Condition[] => {
  if (!conditionStr) return [];

  /**
   * Get field information from field name and metadata
   */
  const getFieldInfo = (fieldname: string): FieldInfo => {
    const meta = fieldsMeta[fieldname];
    const defaultLabel = fieldname
      .replace(/_/g, " ")
      .replace(/\b\w/g, (l) => l.toUpperCase());

    return meta
      ? {
          ...meta,
          value: fieldname,
          fieldname: meta.fieldname || fieldname,
          fieldtype: meta.fieldtype || "Data",
          label: meta.label || defaultLabel,
        }
      : {
          value: fieldname,
          fieldname,
          fieldtype: "Data",
          label: defaultLabel,
        };
  };

  try {
    if (!conditionStr.trim()) return [];

    const conditions: Condition[] = [];
    const parts = conditionStr.split(/\s+(and|or)\s+/i);
    let currentConjunction: "and" | "or" = "and";

    for (let i = 0; i < parts.length; i += 2) {
      const conditionPart = parts[i].trim();
      const nextConjunction = parts[i + 1]?.toLowerCase() as "and" | "or";

      const match = conditionPart.match(
        /^(\w+)\s*([=!<>]+|not\s+in|in|like|not\s+like|is\s+not|is|between|timespan)\s*(.*)$/i
      );

      if (!match) continue;

      const [, fieldname, operator, value] = match;
      const normalizedOperator = operator.toLowerCase().replace(/\s+/g, " ");
      const fieldInfo = getFieldInfo(fieldname);

      const parsedValue = parseConditionValue(value.trim(), normalizedOperator);

      const condition: Condition = {
        field: fieldInfo,
        operator: STRING_TO_OPERATOR[normalizedOperator] || normalizedOperator,
        value: parsedValue,
      };

      if (i > 0) {
        condition.conjunction = currentConjunction;
      }

      conditions.push(condition);

      if (nextConjunction === "and" || nextConjunction === "or") {
        currentConjunction = nextConjunction;
      }
    }

    return conditions;
  } catch (error) {
    console.error("Error parsing condition string:", error);
    return [];
  }
};

/**
 * Parse a condition value string into its appropriate type
 */
function parseConditionValue(value: string, operator: string): unknown {
  if (
    (value.startsWith("'") && value.endsWith("'")) ||
    (value.startsWith('"') && value.endsWith('"'))
  ) {
    return value.slice(1, -1);
  }

  if (["none", "null", "undefined"].includes(value.toLowerCase())) {
    return null;
  }

  if (value === "true") return true;
  if (value === "false") return false;

  const numValue = Number(value);
  if (!isNaN(numValue)) return numValue;

  if (value.startsWith("[") && value.endsWith("]")) {
    return value
      .slice(1, -1)
      .split(",")
      .map((v) => v.trim().replace(/^['"]|['"]$/g, ""));
  }

  return value;
}
