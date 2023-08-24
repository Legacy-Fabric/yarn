package net.legacyfabric.multifilament.task;

import java.io.IOException;
import java.nio.file.FileVisitResult;
import java.nio.file.FileVisitor;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.attribute.BasicFileAttributes;

import javax.inject.Inject;

import org.gradle.api.file.DirectoryProperty;
import org.gradle.api.tasks.InputDirectory;

import net.fabricmc.mappingio.MappingReader;
import net.fabricmc.mappingio.MappingWriter;
import net.fabricmc.mappingio.format.MappingFormat;

import net.legacyfabric.multifilament.mappingsio.SimpleMappingVisitor;

public abstract class DeduplicateMappingsTask extends MappingOutputTask {
	@Inject
	public DeduplicateMappingsTask() {
		this.getOutputFormat().convention(MappingFormat.ENIGMA);
	}

	@InputDirectory
	public abstract DirectoryProperty getInputDir();

	void run(MappingWriter var1) throws IOException {
		SimpleMappingVisitor mappingVisitor = new SimpleMappingVisitor(var1);
		MappingReader.read(this.getInputDir().getAsFile().get().toPath(), mappingVisitor);

		Files.walkFileTree(this.getInputDir().getAsFile().get().toPath(), new FileVisitor<Path>() {
			@Override
			public FileVisitResult preVisitDirectory(Path dir, BasicFileAttributes attrs) throws IOException {
				return FileVisitResult.CONTINUE;
			}

			@Override
			public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
				file.toFile().delete();
				return FileVisitResult.CONTINUE;
			}

			@Override
			public FileVisitResult visitFileFailed(Path file, IOException exc) throws IOException {
				return FileVisitResult.TERMINATE;
			}

			@Override
			public FileVisitResult postVisitDirectory(Path dir, IOException exc) throws IOException {
				dir.toFile().delete();
				return FileVisitResult.CONTINUE;
			}
		});
		this.getInputDir().getAsFile().get().delete();
		Files.move(this.getOutputDir().getAsFile().get().toPath(), this.getInputDir().getAsFile().get().toPath());
	}
}
