import { Route, Routes } from "react-router-dom";
import { Layout } from "../components/Layout";
import { DashboardPage } from "../pages/DashboardPage";
import { UploadPage } from "../pages/UploadPage";
import { ReportPage } from "../pages/ReportPage";

export function App() { return <Layout><Routes><Route path="/" element={<DashboardPage/>}/><Route path="/upload" element={<UploadPage/>}/><Route path="/cases/:caseId" element={<ReportPage/>}/></Routes></Layout> }
