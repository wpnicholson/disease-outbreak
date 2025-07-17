// enums
export type GenderEnum = 'Male' | 'Female' | 'Other';
export type DiseaseCategoryEnum = 'Bacterial' | 'Viral' | 'Parasitic' | 'Other';
export type SeverityLevelEnum = 'Low' | 'Medium' | 'High' | 'Critical';
export type TreatmentStatusEnum = 'None' | 'Ongoing' | 'Completed';
export type ReportStateEnum = 'Draft' | 'Submitted' | 'Under Review' | 'Approved';
export type UserRoleEnum = 'Junior' | 'Senior';

// Reporter
export interface Reporter {
	id: number;  // Is assumed to be the same as `user.id` in the context of the report.
	first_name: string;
	last_name: string;
	email: string;
	job_title: string;
	phone_number: string;
	hospital_name: string;
	hospital_address: string;
	registration_date: string; // ISO string
}

// Patient
export interface Patient {
	id: number;
	first_name: string;
	last_name: string;
	date_of_birth: string; // ISO string
	gender: GenderEnum;
	medical_record_number: string;
	patient_address: string;
	emergency_contact?: string | null;
}

// Disease
export interface Disease {
	id: number;
	disease_name: string;
	disease_category: DiseaseCategoryEnum;
	date_detected: string; // ISO string
	symptoms: string[];
	severity_level: SeverityLevelEnum;
	lab_results?: string | null;
	treatment_status: TreatmentStatusEnum;
}

// Report
export interface Report {
	id: number;
	status: ReportStateEnum;  // from `ReportBase`.
	created_at: string;
	updated_at: string | null;
	reporter: Reporter | null;
	patients: Patient[];
	disease: Disease | null;
}

// User
export interface User {
	id: number;
	email: string;
	full_name?: string;
	is_active: boolean;
	created_at: string;
	updated_at?: string | null;
	role: UserRoleEnum;
}

// Auth Payload (optional helper)
export interface LoginResponse {
	access_token: string;
	token_type: 'bearer';
	user: User;
}

// Audit Log
export interface AuditLog {
	id: number;
	timestamp: string;
	user_id?: number | null;
	action: string;
	entity_type: string;
	entity_id: number;
	changes?: Record<string, unknown> | null;
}

// Statistics Summary
export interface StatisticsSummary {
	total_reports: number;
	reports_by_status: Record<string, number>;
	diseases_by_category: Record<string, number>;
	diseases_by_severity: Record<string, number>;
	average_patient_age?: number | null;
	most_common_disease?: string | null;
}
