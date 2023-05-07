// DO NOT EDIT.
// swift-format-ignore-file
//
// Generated by the protobuf-to-swift
//

import APIKit
import Foundation

// MARK: - Helper
extension Session {

    convenience init(config: URLSessionConfiguration) {
        let adapter = URLSessionAdapter(configuration: config)
        self.init(adapter: adapter)
    }

    /// hostに対しての同時接続数を制限したSession
    static let sharedSerialSession: Session = {
        let config = URLSessionConfiguration.default
        config.httpMaximumConnectionsPerHost = 1
        return .init(config: config)
    }()
}

// MARK: - Swift Concurrency
extension Session {
    func send<T: Request>(_ request: T) async throws -> T.Response {
        let sessionTask: Wrapper<APIKit.SessionTask?> = Wrapper(nil)
        return try await withTaskCancellationHandler {
            try await withCheckedThrowingContinuation { continuation in
                sessionTask.value = send(request) { result in
                    switch result {
                    case let .success(response):
                        continuation.resume(returning: response)
                    case let .failure(error):
                        continuation.resume(throwing: error)
                    }
                }
            }
        } onCancel: {
            sessionTask.value?.cancel()
        }
    }
}

// MARK: - Wrapper
private final class Wrapper<Wrapped> {
    var value: Wrapped
    init(_ value: Wrapped) { self.value = value }
}