# Database Schema

## Tables

### Users
- `id` (Primary Key)
- `name` (VARCHAR, NOT NULL)
- `email` (VARCHAR, UNIQUE, NOT NULL)
- `password_hash` (VARCHAR, NOT NULL)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

### Groups
- `id` (Primary Key)
- `name` (VARCHAR, NOT NULL)
- `subject` (VARCHAR, NOT NULL)
- `description` (TEXT)
- `created_by` (Foreign Key -> Users.id)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

### Group_Members
- `id` (Primary Key)
- `group_id` (Foreign Key -> Groups.id)
- `user_id` (Foreign Key -> Users.id)
- `role` (ENUM: 'admin', 'member')
- `joined_at` (TIMESTAMP)

### Materials
- `id` (Primary Key)
- `title` (VARCHAR, NOT NULL)
- `description` (TEXT)
- `file_path` (VARCHAR)
- `file_type` (VARCHAR)
- `uploaded_by` (Foreign Key -> Users.id)
- `group_id` (Foreign Key -> Groups.id)
- `created_at` (TIMESTAMP)

### AI_Conversations
- `id` (Primary Key)
- `user_id` (Foreign Key -> Users.id)
- `question` (TEXT, NOT NULL)
- `answer` (TEXT, NOT NULL)
- `created_at` (TIMESTAMP)

## Relationships

- Users -> Groups (One-to-Many via created_by)
- Users -> Group_Members (One-to-Many)
- Groups -> Group_Members (One-to-Many)
- Groups -> Materials (One-to-Many)
- Users -> Materials (One-to-Many via uploaded_by)
- Users -> AI_Conversations (One-to-Many)