import streamlit as st
import pandas as pd

# Sample data setup using session state
if "students" not in st.session_state:
    st.session_state.students = [
        {"Id": "S001", "Name": "Abdul Rehman", "Age": "18", "Class": "12A", "CGPA": "2.0"},
        {"Id": "S002", "Name": "Shahzad", "Age": "20", "Class": "12B", "CGPA": "3.5"}
    ]

users = {
    "ahmed": {"password": "teach1", "role": "teacher"},
    "abr": {"password": "std123", "id": "S001", "role": "student"},
    "shahzad": {"password": "std124", "id": "S002", "role": "student"},
}

# Helper functions
def authenticate(username, password):
    user = users.get(username)
    if user and user["password"] == password:
        return user
    return None

def get_student_by_id(sid):
    for student in st.session_state.students:
        if student["Id"] == sid:
            return student
    return None

def teacher_dashboard():
    st.subheader("📋 Teacher Dashboard")

    menu = st.sidebar.radio("Menu", ["View All Students", "Add Student", "Edit Student", "Remove Student", "Logout"])

    if menu == "View All Students":
        st.write("### 📘 Student List")
        df = pd.DataFrame(st.session_state.students)
        st.dataframe(df, use_container_width=True)

    elif menu == "Add Student":
        st.write("### ➕ Add New Student")
        stid = st.text_input("Student ID")
        stname = st.text_input("Name")
        stage = st.text_input("Age")
        stclass = st.text_input("Class")
        stcgpa = st.text_input("CGPA")

        if st.button("Add Student"):
            st.session_state.students.append({
                "Id": stid,
                "Name": stname,
                "Age": stage,
                "Class": stclass,
                "CGPA": stcgpa
            })
            st.success("✅ Student added successfully!")

    elif menu == "Edit Student":
        st.write("### ✏️ Edit Student")
        stid = st.text_input("Enter Student ID to Edit")
        student = get_student_by_id(stid)
        if student:
            stname = st.text_input("Name", student["Name"])
            stage = st.text_input("Age", student["Age"])
            stclass = st.text_input("Class", student["Class"])
            stcgpa = st.text_input("CGPA", student["CGPA"])

            if st.button("Update Student"):
                student["Name"] = stname
                student["Age"] = stage
                student["Class"] = stclass
                student["CGPA"] = stcgpa
                st.success("✅ Student updated successfully!")
        else:
            st.warning("⚠️ Student not found.")

    elif menu == "Remove Student":
        st.write("### ❌ Remove Student")
        stid = st.text_input("Enter Student ID to Delete")
        if st.button("Delete"):
            found = False
            for student in st.session_state.students:
                if student["Id"] == stid:
                    st.session_state.students.remove(student)
                    st.success("✅ Student removed successfully!")
                    found = True
                    break
            if not found:
                st.warning("⚠️ Student not found.")

def student_dashboard(sid):
    st.subheader("🎓 Student Dashboard")
    student = get_student_by_id(sid)
    if student:
        st.write(f"**ID:** {student['Id']}")
        st.write(f"**Name:** {student['Name']}")
        st.write(f"**Age:** {student['Age']}")
        st.write(f"**Class:** {student['Class']}")
        st.write(f"**CGPA:** {student['CGPA']}")
    else:
        st.warning("⚠️ Student record not found.")

# Streamlit UI
def main():
    st.title("🎓 Student Management System")

    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is None:
        st.subheader("🔐 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = authenticate(username, password)
            if user:
                st.session_state.user = user
                st.success(f"✅ Welcome, {username}!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password.")
    else:
        user = st.session_state.user
        if user["role"] == "teacher":
            teacher_dashboard()
        elif user["role"] == "student":
            student_dashboard(user["id"])

        if st.sidebar.button("🚪 Logout"):
            st.session_state.user = None
            st.rerun()

if __name__ == "__main__":
    main()
