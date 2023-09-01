from src.data_source.interface import DataSource
from typing import Iterator, Tuple, Optional
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class GoogleSheetsDataSource(DataSource):
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

    def __init__(
        self, spreadsheet_id: str, range_name: str, credentials_path: str
    ) -> None:
        self.spreadsheet_id = spreadsheet_id
        self.range_name = range_name
        self.credentials_path = credentials_path
        self.creds = None

        # Authenticate and create the service client.
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                self.creds = pickle.load(token)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            with open("token.pickle", "wb") as token:
                pickle.dump(self.creds, token)

        self.service = build("sheets", "v4", credentials=self.creds)

    @staticmethod
    def format_row(self, row: list) -> Tuple[str, str]:
        return str(row[0]), "\n".join(map(str, row))

    def get_documents(self) -> Iterator[Tuple[str, str]]:
        sheet = self.service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=self.spreadsheet_id, range=self.range_name)
            .execute()
        )
        values = result.get("values", [])
        if not values:
            print("No data found.")
        else:
            for row in values:
                yield self.format_row(row)

    def listen_for_updates(self) -> Iterator[Tuple[str, str]]:
        raise NotImplementedError("no direct easy way")
