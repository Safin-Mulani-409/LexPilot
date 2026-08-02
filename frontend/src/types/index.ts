export type Status = "uploaded" | "processing" | "ready" | "failed";
export interface Party { name: string; role: string }
export interface SourcedItem { text: string; page_references: number[] }
export interface TimelineEvent { date: string | null; event: string; page_references: number[] }
export interface LegalIssue { issue: string; context: string }
export interface Analysis { case_summary: string; parties: Party[]; important_facts: SourcedItem[]; timeline: TimelineEvent[]; legal_issues: LegalIssue[]; missing_information: string[]; suggested_questions: string[]; hearing_preparation_checklist: string[]; next_steps: string[]; disclaimer: string }
export interface Report { id: string; case_id: string; status: Status; analysis: Analysis | null; error_message: string | null; created_at: string; completed_at: string | null }
export interface Case { id: string; title: string; original_filename: string; status: Status; created_at: string; page_count?: number; latest_report?: Report | null }
